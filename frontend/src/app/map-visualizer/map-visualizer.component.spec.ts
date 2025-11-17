import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MapVisualizerComponent } from './map-visualizer.component';

describe('MapVisualizerComponent', () => {
  let component: MapVisualizerComponent;
  let fixture: ComponentFixture<MapVisualizerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MapVisualizerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MapVisualizerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
