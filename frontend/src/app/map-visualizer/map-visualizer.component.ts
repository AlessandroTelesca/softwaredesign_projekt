import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-map-visualizer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './map-visualizer.component.html',
  styleUrls: ['./map-visualizer.component.css']
})
export class MapVisualizerComponent implements OnInit {
  message: string = '';
  loading: boolean = false;
  error: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.callApi();
  }

  callApi(): void {
    this.loading = true;
    this.error = '';
    this.http.get<any>('http://127.0.0.1:5000/api/hello')
      .subscribe({
        next: (response) => {
          this.message = JSON.stringify(response);
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Error: ' + err.message;
          this.loading = false;
        }
      });
  }
}
