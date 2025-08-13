import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgIf } from '@angular/common';

export interface AppStatistics {
  total_countries: number;
  total_institutions: number;
  total_speeches: number;
  total_speakers: number;
  total_protocols: number;
}

@Component({
  selector: 'app-dashboard',
  imports: [NgIf],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard implements OnInit {
  stats: AppStatistics | null = null;
  loading = true;
  error: string | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.fetchStatistics();
  }

  fetchStatistics() {
    this.loading = true;
    this.http.get<AppStatistics>('/api/app_statistics').subscribe({
      next: (data) => {
        this.stats = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load statistics.';
        this.loading = false;
      }
    });
  }
}
