import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { TabsPage } from './tabs.page';

// As três telas internas ficam como "filhas" da tela de abas. Cada uma é
// carregada sob demanda quando o usuário toca na aba correspondente.
const routes: Routes = [
  {
    path: '',
    component: TabsPage,
    children: [
      {
        path: 'medicoes',
        loadChildren: () =>
          import('../medicoes/medicoes.module').then((m) => m.MedicoesPageModule),
      },
      {
        path: 'relatorio',
        loadChildren: () =>
          import('../relatorio/relatorio.module').then(
            (m) => m.RelatorioPageModule
          ),
      },
      {
        path: 'integrantes',
        loadChildren: () =>
          import('../integrantes/integrantes.module').then(
            (m) => m.IntegrantesPageModule
          ),
      },
      { path: '', redirectTo: 'medicoes', pathMatch: 'full' },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class TabsPageRoutingModule {}
