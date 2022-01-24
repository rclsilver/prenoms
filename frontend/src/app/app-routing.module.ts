import { NgModule } from '@angular/core';
import { ExtraOptions, RouterModule, Routes } from '@angular/router';
import { FirstStageResultComponent } from './components/first-stage-result/first-stage-result.component';
import { FirstStageVoteComponent } from './pages/first-stage-vote/first-stage-vote.component';
import { GameListComponent } from './pages/game-list/game-list.component';

const routes: Routes = [
  {
    path: 'games',
    children: [
      {
        path: '',
        component: GameListComponent,
      },
      {
        path: ':id',
        children: [
          {
            path: '',
            component: FirstStageVoteComponent,
          },
          {
            path: 'results',
            component: FirstStageResultComponent,
          },
        ],
      },
    ],
  },
];

const config: ExtraOptions = {
  useHash: true,
};

@NgModule({
  imports: [RouterModule.forRoot(routes, config)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
