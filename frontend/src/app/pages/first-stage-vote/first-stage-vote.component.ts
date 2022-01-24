import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { Name } from 'src/app/models/name.model';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-first-stage-vote',
  templateUrl: './first-stage-vote.component.html',
  styleUrls: ['./first-stage-vote.component.scss'],
})
export class FirstStageVoteComponent implements OnInit {
  private _loading$ = new BehaviorSubject<boolean>(false);
  readonly loading$ = this._loading$.asObservable();

  private _current$ = new BehaviorSubject<Name | null>(null);
  readonly current$ = this._current$.asObservable();

  gameId?: string;

  constructor(private _api: ApiService, private _route: ActivatedRoute) {}

  ngOnInit(): void {
    this._route.params.subscribe((params) => {
      this.gameId = params.id;
      this.next();
    });
  }

  next(): void {
    this._loading$.next(true);
    this._api.getFirstStageNext(this.gameId!).subscribe(
      (name) => {
        this._current$.next(name);
      },
      (e) => {
        console.error(e);
      },
      () => {
        this._loading$.next(false);
      }
    );
  }

  like(name: Name): void {
    this._loading$.next(true);
    this._api.firstStageVote(this.gameId!, name, true).subscribe(
      () => {
        this.next();
      },
      (e) => {
        console.error(e);
      },
      () => {
        this._loading$.next(false);
      }
    );
  }

  dislike(name: Name): void {
    this._loading$.next(true);
    this._api.firstStageVote(this.gameId!, name, false).subscribe(
      () => {
        this.next();
      },
      (e) => {
        console.error(e);
      },
      () => {
        this._loading$.next(false);
      }
    );
  }
}
