import { AfterViewInit, Component, ElementRef, OnDestroy, ViewChild } from '@angular/core';
import * as THREE from 'three';

@Component({
  selector: 'app-robot-visualizer',
  standalone: true,
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

  // rotation control variable
  public rotationEnabled = false;

  private lightMeshes: THREE.Mesh[] = [];
  private flashColor = new THREE.Color(0xff0000); // red flash

  // start disabled so a button can trigger flashing
  private flashEnabled = false;
  private lastToggleTime = 0;
  private lightsOn = false;

  ngAfterViewInit(): void {
    this.initThree();
    this.startAnimationLoop();
    window.addEventListener('resize', this.onWindowResize);
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onWindowResize);
    if (this.frameId !== null) {
      cancelAnimationFrame(this.frameId);
    }
    this.renderer?.dispose();
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

    const gltfModule = await import('three/examples/jsm/loaders/GLTFLoader');

    const GLTFLoaderClass = (gltfModule as any).GLTFLoader;
    const loader = new GLTFLoaderClass();

    const modelUrl = '/assets/robot.gltf';
    loader.load(
      modelUrl,
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

  // public method to toggle rotation
  public toggleRotation(): void {
    this.rotationEnabled = !this.rotationEnabled;
  }

  private startAnimationLoop = () => {
    this.frameId = requestAnimationFrame(this.startAnimationLoop);

    // Render
    this.renderer.render(this.scene, this.camera);

    // ROTATION: only rotate when enabled
    if (this.robotModel && this.rotationEnabled) {
      this.robotModel.rotation.y += 0.002;
    }

    // call flashing each frame
    this.applyLightFlashing();
  };

  private onWindowResize = () => {
    const width = this.container.nativeElement.clientWidth || 800;
    const height = this.container.nativeElement.clientHeight || 600;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  };


}
