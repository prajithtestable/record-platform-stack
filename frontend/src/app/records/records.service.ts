import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { RecordDto } from './record.model';

@Injectable({ providedIn: 'root' })
export class RecordsService {
  private readonly baseUrl = `${environment.apiBaseUrl}/records`;

  constructor(private readonly http: HttpClient) {}

  list(): Observable<RecordDto[]> {
    return this.http.get<RecordDto[]>(this.baseUrl);
  }

  create(title: string, description: string): Observable<RecordDto> {
    return this.http.post<RecordDto>(this.baseUrl, { title, description });
  }
}
