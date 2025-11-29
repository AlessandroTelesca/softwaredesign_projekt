import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-map-visualizer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './map-visualizer.component.html',
  styleUrls: ['./map-visualizer.component.css']
})
export class MapVisualizerComponent implements OnInit {
  mapHtml: SafeHtml | null = null;
  loading: boolean = true;
  error: string = '';

  constructor(private sanitizer: DomSanitizer) {}

  ngOnInit(): void {
    const api = 'http://127.0.0.1:5000/api/map';

    fetch(api)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!data || !data.map) throw new Error('No map in response');
        this.mapHtml = this.sanitizer.bypassSecurityTrustHtml(data.map);
        this.loading = false;
      })
      .catch((err) => {
        this.error = `Failed to load map: ${err}`;
        this.loading = false;
      });
  }

  onLoad(): void {
    this.loading = false;
  }

  reload(): void {
    this.loading = true;
    this.error = '';
    this.mapHtml = null;
    const api = 'http://127.0.0.1:5000/api/map';
    fetch(api)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!data || !data.map) throw new Error('No map in response');
        this.mapHtml = this.sanitizer.bypassSecurityTrustHtml(data.map);
        this.loading = false;
      })
      .catch((err) => {
        this.error = `Failed to load map: ${err}`;
        this.loading = false;
      });
  }
}
