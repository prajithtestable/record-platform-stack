import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RecordsService } from './records.service';
import { RecordDto } from './record.model';

@Component({
  selector: 'app-records-page',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './records-page.html',
})
export class RecordsPage implements OnInit {
  readonly records = signal<RecordDto[]>([]);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);

  title = '';
  description = '';

  constructor(private readonly recordsService: RecordsService) {}

  ngOnInit(): void {
    this.refresh();
  }

  refresh(): void {
    this.loading.set(true);
    this.error.set(null);
    this.recordsService.list().subscribe({
      next: (records) => {
        this.records.set(records);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set('Could not reach backend-service-a: ' + err.message);
        this.loading.set(false);
      },
    });
  }

  submit(): void {
    if (!this.title.trim()) return;
    this.recordsService.create(this.title.trim(), this.description.trim()).subscribe({
      next: () => {
        this.title = '';
        this.description = '';
        this.refresh();
      },
      error: (err) => this.error.set('Could not create record: ' + err.message),
    });
  }
}
