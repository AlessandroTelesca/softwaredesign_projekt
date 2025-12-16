import { AfterViewInit, Component, ElementRef, OnDestroy, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import * as THREE from 'three';
// import GLTFLoader from 'three/examples/jsm/loaders/GLTFLoader';
import { RobotService, RobotStatus } from './robot.service';

@Component({
  selector: 'app-robot-visualizer',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './robot-visualizer.component.html',
  styleUrls: ['./robot-visualizer.component.css']
})
export class RobotVisualizerComponent implements AfterViewInit, OnDestroy {
  @ViewChild('canvasContainer', { static: true }) container!: ElementRef<HTMLDivElement>;

  private renderer!: THREE.WebGLRenderer;
  private scene!: THREE.Scene;
  private camera!: THREE.PerspectiveCamera;
  private frameId: number | null = null;
  private robotModel: THREE.Object3D | null = null;
  private tramModel: THREE.Object3D | null = null;
  private controls: any;
  private lightMeshes: THREE.Mesh[] = [];
  private flashColor = new THREE.Color(0xff0000); // red flash

  // start disabled so a button can trigger flashing
  private flashEnabled = false;
  private lastToggleTime = 0;
  private lightsOn = false;
  public robotId = 0;
  public robotStatus: RobotStatus | null = null;
  public loading = false;
  public error: string | null = null;

  constructor(private robotService: RobotService) {}

  ngAfterViewInit(): void {
    this.initThree();
    this.startAnimationLoop();
    window.addEventListener('resize', this.onWindowResize);

    // Optionally load initial robot status (id 0)
    this.loadRobotStatus();
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onWindowResize);
    if (this.frameId !== null) {
      cancelAnimationFrame(this.frameId);
    }
    this.renderer?.dispose();
    this.controls?.dispose && this.controls.dispose();
  }

  public loadRobotStatus(id: number = this.robotId, allowCreate: boolean = true): void {
    this.loading = true;
    this.error = null;
    this.robotService.getRobotStatus(id).subscribe({
      next: (resp) => {
        if (resp.error) {
          // if none exists or out of range, create and retry once
          if (allowCreate && (resp.error.includes('No robots available') || resp.error.includes('out of range'))) {
            this.createAndReload();
            return;
          }
          this.robotStatus = null;
          this.error = resp.error;
        } else if (resp.status) {
          this.robotStatus = resp.status;
        } else {
          this.robotStatus = null;
        }
        this.loading = false;
      },
      error: (err) => {
        // Try to read backend-provided error message
        const backendMsg: string | undefined = err?.error?.error || err?.error?.message;
        if (
          allowCreate && backendMsg && (backendMsg.includes('No robots available') || backendMsg.includes('out of range'))
        ) {
          this.createAndReload();
          return;
        }
        this.loading = false;
        this.robotStatus = null;
        this.error = backendMsg || (err?.message) || 'Unbekannter Fehler beim Laden des Roboters.';
      }
    });
  }

  private createAndReload(): void {
    this.robotService.createRobot().subscribe({
      next: (res) => {
        this.robotId = typeof res?.robot_id === 'number' ? res.robot_id : 0;
        // retry load once without creating again
        this.loadRobotStatus(this.robotId, false);
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.error || err?.message || 'Roboter konnte nicht erstellt werden.';
      }
    });
  }

  private async initThree() {
    const width = this.container.nativeElement.clientWidth || 800;
    const height = this.container.nativeElement.clientHeight || 600;

    // Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setPixelRatio(window.devicePixelRatio || 1);
    this.renderer.setSize(width, height);
    this.container.nativeElement.appendChild(this.renderer.domElement);

    // Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0xf0f0f0);

    // Camera
    this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    this.camera.position.set(0, 1, 2);

    this.camera.lookAt(new THREE.Vector3(0, 0.5, 0));

    // OrbitControls (dynamically imported so example module is loaded at runtime)
    try {
      const orbitModule = await import('three/examples/jsm/controls/OrbitControls.js');
      const OrbitControlsClass = (orbitModule as any).OrbitControls;
      this.controls = new OrbitControlsClass(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.05;
      this.controls.screenSpacePanning = false;
      this.controls.minDistance = 0.5;
      this.controls.maxDistance = 10;
      this.controls.target.set(0, 0.5, 0);
      this.controls.update();
    } catch (e) {
      console.warn('OrbitControls not available', e);
    }

    // Lights
    const hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 0.6);
    hemi.position.set(0, 20, 0);
    this.scene.add(hemi);

    const dir = new THREE.DirectionalLight(0xffffff, 0.8);
    dir.position.set(3, 10, 10);
    this.scene.add(dir);

    // Ground grid
    const grid = new THREE.GridHelper(10, 10, 0x888888, 0xdddddd);
    this.scene.add(grid);
    grid.position.y = -1;

    const gltfModule = await import('three/examples/jsm/loaders/GLTFLoader.js');

    const GLTFLoaderClass = (gltfModule as any).GLTFLoader;
    const RobotLoader = new GLTFLoaderClass();

    const RobotModelUrl = '/assets/robot.gltf';
    RobotLoader.load(
      RobotModelUrl,
      (gltf: any) => {
        this.robotModel = gltf.scene || (gltf.scenes && gltf.scenes[0]);
        if (this.robotModel) {
          this.robotModel.position.set(0, 0, 0);
          this.robotModel.rotation.y = -Math.PI/2;
          this.scene.add(this.robotModel);

          // find meshes named "light"
          this.robotModel.traverse((child: any) => {
            if (child && child.isMesh) {
              const name = (child.name || '').toLowerCase();
              const matName = (child.material && child.material.name || '').toLowerCase();

              if (name.includes('light')) {
                // clone material so changes only affect this mesh
                let mat = child.material.clone();
                if (!('emissive' in mat)) {
                  const baseColor = (mat.color && mat.color.clone()) || new THREE.Color(0xffffff);
                  mat = new THREE.MeshStandardMaterial({ color: baseColor });
                }
                mat.emissive = mat.emissive || new THREE.Color(0x000000);
                (mat as any).emissiveIntensity = 1;
                child.material = mat;
                this.lightMeshes.push(child);
              }
            }
          });
        }
      }
    );

    const TramLoader = new GLTFLoaderClass();
    const TramModelUrl = '/assets/bahn.gltf';
    TramLoader.load(
      TramModelUrl,
      (gltf: any) => {
        this.tramModel = gltf.scene || (gltf.scenes && gltf.scenes[0]);
        if (this.tramModel) {
          this.tramModel.position.set(-10.5, 0.5, 0.7);
          this.scene.add(this.tramModel);
          this.ToggleTramModel(false);
        }
      }
    );
  }

  public ToggleTramModel(visible?: boolean) {
    if (!this.tramModel) return;

    if (typeof visible === 'boolean') {
      this.tramModel.visible = visible;
    } else {
      this.tramModel.visible = !this.tramModel.visible;
    }
  }

  // methods to toggle light flashing and flashing logic
  public toggleFlashing(): void {
    this.flashEnabled = !this.flashEnabled;

    if (this.flashEnabled) {
      this.lastToggleTime = 0;
      this.lightsOn = false;
    } else {
      const offColor = new THREE.Color(0x000000);
      this.lightMeshes.forEach(mesh => {
        const mat: any = mesh.material;
        if (mat && mat.emissive) {
          mat.emissive.copy(offColor);
          mat.needsUpdate = true;
        }
      });
      this.lightsOn = false;
    }
  }
  private applyLightFlashing() {
    if (!this.flashEnabled || this.lightMeshes.length === 0) return;

    const now = performance.now() / 250; // seconds

    if (now - this.lastToggleTime >= 1) {
      this.lightsOn = !this.lightsOn;
      this.lastToggleTime = now;
    }

    const targetColor = this.lightsOn ? this.flashColor : new THREE.Color(0x000000);
    this.lightMeshes.forEach(mesh => {
      const mat: any = mesh.material;
      if (mat && mat.emissive) {
        mat.emissive.copy(targetColor);
        mat.needsUpdate = true;
      }
    });
  }

  private batteryStatus() {
    if (!this.robotStatus?.battery_status) return;
    // Could visualize battery level (e.g., change LED color based on level)
    // For now, just log or store for UI display
  }

  private isCharging() {
    if (!this.robotStatus?.is_charging) return;
    // Visual indicator: could pulse lights or change color
    // Example: set LED to green when charging
    if (this.lightMeshes.length > 0) {
      const chargingColor = new THREE.Color(0x00ff00); // green
      this.lightMeshes.forEach(mesh => {
        const mat: any = mesh.material;
        if (mat && mat.emissive && !this.flashEnabled) {
          mat.emissive.copy(chargingColor);
          mat.needsUpdate = true;
        }
      });
    }
  }

  private isDoorOpened() {
    if (!this.robotStatus?.is_door_opened) return;
    // Could trigger door animation or visual cue
    // For now, just a placeholder for future door mechanics
  }

  private isParked() {
    if (!this.robotStatus?.is_parked) return;
    // Show tram when robot is parked (as if it's at a tram stop)
    this.ToggleTramModel(true);
  }

  private isReversing() {
    if (!this.robotStatus?.is_reversing) return;
    // Enable flashing lights when reversing
    if (!this.flashEnabled) {
      this.flashEnabled = true;
      this.lastToggleTime = 0;
    }
  }

  private message() {
    if (!this.robotStatus?.message) return;
    // Message is already displayed in the UI via robotStatus
    // Could add console log for debugging
    // console.log('Robot message:', this.robotStatus.message);
  }

  private packages() {
    if (!this.robotStatus?.packages || this.robotStatus.packages.length === 0) return;
    // Could visualize package count or details
  }

  private applyStatusVisuals() {
    if (!this.robotStatus) return;

    // Reset visuals first
    if (!this.robotStatus.is_reversing && this.flashEnabled) {
      this.flashEnabled = false;
      const offColor = new THREE.Color(0x000000);
      this.lightMeshes.forEach(mesh => {
        const mat: any = mesh.material;
        if (mat && mat.emissive) {
          mat.emissive.copy(offColor);
          mat.needsUpdate = true;
        }
      });
    }

    if (!this.robotStatus.is_parked) {
      this.ToggleTramModel(false);
    }

    // Apply status-driven visuals
    this.batteryStatus();
    this.isCharging();
    this.isDoorOpened();
    this.isParked();
    this.isReversing();
    this.message();
    this.packages();
  }

  private startAnimationLoop = () => {
    this.frameId = requestAnimationFrame(this.startAnimationLoop);

    // Update controls (if available)
    this.controls?.update && this.controls.update();

    // Apply robot status-driven visuals
    this.applyStatusVisuals();

    // call flashing each frame
    this.applyLightFlashing();

    // Render
    this.renderer.render(this.scene, this.camera);
  };

  private onWindowResize = () => {
    const width = this.container.nativeElement.clientWidth || 800;
    const height = this.container.nativeElement.clientHeight || 600;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  };


}
