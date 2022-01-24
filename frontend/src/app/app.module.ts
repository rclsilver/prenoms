import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { VoteCardComponent } from './components/vote-card/vote-card.component';
import { FirstStageVoteComponent } from './pages/first-stage-vote/first-stage-vote.component';
import { TopMenuComponent } from './components/top-menu/top-menu.component';
import { GameListComponent } from './pages/game-list/game-list.component';
import { FirstStageResultComponent } from './components/first-stage-result/first-stage-result.component';

@NgModule({
  declarations: [AppComponent, VoteCardComponent, FirstStageVoteComponent, TopMenuComponent, GameListComponent, FirstStageResultComponent],
  imports: [BrowserModule, AppRoutingModule, HttpClientModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
