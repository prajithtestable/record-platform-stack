import { Component } from '@angular/core';
import { RecordsPage } from './records/records-page';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RecordsPage],
  template: `<app-records-page></app-records-page>`,
})
export class App {
  protected readonly title = 'frontend';
}
