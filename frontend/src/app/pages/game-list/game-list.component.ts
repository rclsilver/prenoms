import { Component, OnInit } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Game } from 'src/app/models/game.model';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-game-list',
  templateUrl: './game-list.component.html',
  styleUrls: ['./game-list.component.scss'],
})
export class GameListComponent implements OnInit {
  private _games$ = new BehaviorSubject<Game[]>([]);
  readonly games$ = this._games$.asObservable();

  constructor(private _api: ApiService) {}

  refresh(): void {
    this._api.getGames().subscribe((games) => this._games$.next(games));
  }

  ngOnInit(): void {
    this.refresh();
  }
}
