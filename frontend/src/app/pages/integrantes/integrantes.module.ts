import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';

import { IntegrantesPage } from './integrantes.page';
import { IntegrantesPageRoutingModule } from './integrantes-routing.module';

@NgModule({
  imports: [CommonModule, IonicModule, IntegrantesPageRoutingModule],
  declarations: [IntegrantesPage],
})
export class IntegrantesPageModule {}
