import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Name } from 'src/app/models/name.model';

@Component({
  selector: 'app-vote-card',
  templateUrl: './vote-card.component.html',
  styleUrls: ['./vote-card.component.scss'],
})
export class VoteCardComponent implements OnInit {
  private _loading$ = new BehaviorSubject<boolean | null>(false);
  readonly loading$ = this._loading$.asObservable();

  @Input() name?: Name;
  @Input() set loading(loading: boolean | null) {
    this._loading$.next(loading);
  }
  @Output() onLike = new EventEmitter<Name>();
  @Output() onDislike = new EventEmitter<Name>();

  constructor() {}

  ngOnInit(): void {}

  like(name: Name): void {
    this.onLike.emit(name);
  }

  dislike(name: Name): void {
    this.onDislike.emit(name);
  }
}
