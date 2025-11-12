import { Component } from '@angular/core';
import { RobotVisualizerComponent } from './robot-visualizer/robot-visualizer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RobotVisualizerComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';
}
