import { Routes } from '@angular/router';
import { RobotVisualizerComponent } from './robot-visualizer/robot-visualizer.component';
import { MapVisualizerComponent } from './map-visualizer/map-visualizer.component';

export const routes: Routes = [
	{ path: '', redirectTo: 'robot', pathMatch: 'full' },
	{ path: 'robot', component: RobotVisualizerComponent },
	{ path: 'map', component: MapVisualizerComponent },
];
