import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-map-visualizer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './map-visualizer.component.html',
  styleUrls: ['./map-visualizer.component.css']
})
export class MapVisualizerComponent implements OnInit {
  mapUrl: SafeResourceUrl | null = null;
  loading: boolean = true;
  error: string = '';

  constructor(private sanitizer: DomSanitizer) {}

  ngOnInit(): void {
    const url = 'http://127.0.0.1:5000/';
    this.mapUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }

  onLoad(): void {
    this.loading = false;
  }

  reload(): void {
    this.loading = true;
    this.mapUrl = this.sanitizer.bypassSecurityTrustResourceUrl('http://127.0.0.1:5000/');
  }
}
