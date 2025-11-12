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
