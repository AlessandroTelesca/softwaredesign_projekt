import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RobotVisualizerComponent } from './robot-visualizer.component';

describe('RobotVisualizerComponent', () => {
  let component: RobotVisualizerComponent;
  let fixture: ComponentFixture<RobotVisualizerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RobotVisualizerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RobotVisualizerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
