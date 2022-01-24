import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Game } from '../models/game.model';
import { Name } from '../models/name.model';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private _http: HttpClient) {}

  getGames(): Observable<Game[]> {
    return this._http.get<Game[]>('/api/games');
  }

  getFirstStageNext(gameId: string): Observable<Name | null> {
    return this._http.get<Name>(`/api/games/${gameId}/stage-1/next`);
  }

  getFirstStageResult(gameId: string): Observable<Name[]> {
    return this._http.get<Name[]>(`/api/games/${gameId}/stage-1/result`);
  }

  firstStageVote(
    gameId: string,
    name: Name,
    choice: boolean
  ): Observable<void> {
    return this._http.post<void>(`/api/games/${gameId}/stage-1`, {
      name_id: name.id,
      choice,
    });
  }
}
