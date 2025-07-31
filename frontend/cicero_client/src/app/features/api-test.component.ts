import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  CommonService, 
  ContextService, 
  TextService 
} from '../core/services';
import { 
  Country, 
  Institution, 
  Protocol 
} from '../core/models';

@Component({
  selector: 'app-api-test',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="api-test-container">
      <h2>API Connection Test</h2>
      
      <div class="test-section">
        <h3>Database Seeding</h3>
        <button (click)="testSeedDefaults()" [disabled]="loading">
          Seed Database
        </button>
        <div *ngIf="seedResult" class="result">
          <pre>{{ seedResult | json }}</pre>
        </div>
      </div>

      <div class="test-section">
        <h3>Health Check</h3>
        <button (click)="testHealthCheck()" [disabled]="loading">
          Test Health Check
        </button>
        <div *ngIf="healthResult" class="result">
          <pre>{{ healthResult | json }}</pre>
        </div>
      </div>

      <div class="test-section">
        <h3>Countries</h3>
        <button (click)="testCountries()" [disabled]="loading">
          Load Countries
        </button>
        <div *ngIf="countries" class="result">
          <p>Found {{ countries.length }} countries:</p>
          <ul>
            <li *ngFor="let country of countries">
              {{ country.country }} ({{ country.id }})
            </li>
          </ul>
        </div>
      </div>

      <div class="test-section">
        <h3>Institutions</h3>
        <button (click)="testInstitutions()" [disabled]="loading">
          Load Institutions
        </button>
        <div *ngIf="institutions" class="result">
          <p>Found {{ institutions.length }} institutions:</p>
          <ul>
            <li *ngFor="let institution of institutions">
              {{ institution.label }} ({{ institution.type }})
            </li>
          </ul>
        </div>
      </div>

      <div class="test-section">
        <h3>Protocols</h3>
        <button (click)="testProtocols()" [disabled]="loading">
          Load Protocols
        </button>
        <div *ngIf="protocols" class="result">
          <p>Found {{ protocols.length }} protocols:</p>
          <ul>
            <li *ngFor="let protocol of protocols">
              {{ protocol.date | date }} - {{ protocol.protocol_type }}
            </li>
          </ul>
        </div>
      </div>

      <div *ngIf="error" class="error">
        <h4>Error:</h4>
        <p>{{ error }}</p>
      </div>
    </div>
  `,
  styles: [`
    .api-test-container {
      padding: 20px;
      max-width: 800px;
      margin: 0 auto;
    }

    .test-section {
      margin-bottom: 30px;
      padding: 15px;
      border: 1px solid #ddd;
      border-radius: 5px;
    }

    .test-section h3 {
      margin-top: 0;
      color: #333;
    }

    button {
      background-color: #007bff;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 4px;
      cursor: pointer;
    }

    button:hover:not(:disabled) {
      background-color: #0056b3;
    }

    button:disabled {
      background-color: #6c757d;
      cursor: not-allowed;
    }

    .result {
      margin-top: 15px;
      padding: 10px;
      background-color: #f8f9fa;
      border-radius: 4px;
    }

    .result pre {
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    .result ul {
      margin: 0;
      padding-left: 20px;
    }

    .error {
      background-color: #f8d7da;
      border: 1px solid #f5c6cb;
      color: #721c24;
      padding: 15px;
      border-radius: 4px;
    }
  `]
})
export class ApiTestComponent implements OnInit {
  loading = false;
  error: string | null = null;
  
  seedResult: any = null;
  healthResult: any = null;
  countries: Country[] = [];
  institutions: Institution[] = [];
  protocols: Protocol[] = [];

  constructor(
    private commonService: CommonService,
    private contextService: ContextService,
    private textService: TextService
  ) {}

  ngOnInit(): void {
    // Component initialization
  }

  testSeedDefaults(): void {
    this.loading = true;
    this.error = null;
    
    this.commonService.seedDefaults().subscribe({
      next: (result: any) => {
        this.seedResult = result;
        this.loading = false;
      },
      error: (error: any) => {
        this.error = error.message;
        this.loading = false;
      }
    });
  }

  testHealthCheck(): void {
    this.loading = true;
    this.error = null;
    
    this.commonService.getHealthCheck().subscribe({
      next: (result: any) => {
        this.healthResult = result;
        this.loading = false;
      },
      error: (error: any) => {
        this.error = error.message;
        this.loading = false;
      }
    });
  }

  testCountries(): void {
    this.loading = true;
    this.error = null;
    
    this.contextService.getCountries().subscribe({
      next: (countries: Country[]) => {
        this.countries = countries;
        this.loading = false;
      },
      error: (error: any) => {
        this.error = error.message;
        this.loading = false;
      }
    });
  }

  testInstitutions(): void {
    this.loading = true;
    this.error = null;
    
    this.contextService.getInstitutions().subscribe({
      next: (institutions: Institution[]) => {
        this.institutions = institutions;
        this.loading = false;
      },
      error: (error: any) => {
        this.error = error.message;
        this.loading = false;
      }
    });
  }

  testProtocols(): void {
    this.loading = true;
    this.error = null;
    
    this.textService.getProtocols().subscribe({
      next: (protocols: Protocol[]) => {
        this.protocols = protocols;
        this.loading = false;
      },
      error: (error: any) => {
        this.error = error.message;
        this.loading = false;
      }
    });
  }
}
