import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { Name } from 'src/app/models/name.model';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-first-stage-result',
  templateUrl: './first-stage-result.component.html',
  styleUrls: ['./first-stage-result.component.scss'],
})
export class FirstStageResultComponent implements OnInit {
  private _names$ = new BehaviorSubject<Name[]>([]);
  readonly names$ = this._names$.asObservable();

  gameId?: string;

  constructor(private _api: ApiService, private _route: ActivatedRoute) {}

  refresh(): void {
    this._api.getFirstStageResult(this.gameId!).subscribe((result) => {
      this._names$.next(result);
    });
  }

  ngOnInit(): void {
    this._route.params.subscribe((params) => {
      this.gameId = params.id;
      this.refresh();
    });
    this.refresh();
  }
}
