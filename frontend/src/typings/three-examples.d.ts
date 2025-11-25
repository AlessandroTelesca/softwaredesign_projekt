declare module 'three/examples/jsm/loaders/GLTFLoader' {
	import { LoadingManager } from 'three';

	export interface GLTF {
		scene: any;
		scenes: any[];
		animations: any[];
		parser?: any;
	}

	export class GLTFLoader {
		constructor(manager?: LoadingManager);
		load(
			url: string,
			onLoad: (gltf: GLTF) => void,
			onProgress?: (event: ProgressEvent) => void,
			onError?: (event: ErrorEvent) => void
		): void;
		parse(
			data: ArrayBuffer | string,
			path: string,
			onLoad: (gltf: GLTF) => void,
			onError?: (event: ErrorEvent) => void
		): void;
	}

	export { GLTFLoader };
	export default GLTFLoader;
}

declare module 'three/examples/jsm/controls/OrbitControls' {
	import { Camera, EventDispatcher, MOUSE, TOUCH } from 'three';

	export interface OrbitControls extends EventDispatcher {
		object: Camera;
		domElement: HTMLElement;
		enabled: boolean;
		target: { x: number; y: number; z: number };
		enableDamping: boolean;
		dampingFactor: number;
		screenSpacePanning: boolean;
		minDistance: number;
		maxDistance: number;
		mouseButtons: { LEFT: MOUSE; MIDDLE: MOUSE; RIGHT: MOUSE };
		touches: { ONE: TOUCH; TWO: TOUCH };
		update(): void;
		dispose(): void;
	}

	export class OrbitControls {
		constructor(object: Camera, domElement?: HTMLElement);
		object: Camera;
		domElement: HTMLElement;
		enabled: boolean;
		target: { x: number; y: number; z: number };
		enableDamping: boolean;
		dampingFactor: number;
		screenSpacePanning: boolean;
		minDistance: number;
		maxDistance: number;
		update(): void;
		dispose(): void;
	}

	export default OrbitControls;
}
