import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-integrantes',
  standalone: false,
  templateUrl: './integrantes.page.html',
  styleUrls: ['./integrantes.page.scss'],
})
export class IntegrantesPage {
  // Lista exibida na tela. Manter os nomes num array facilita renderizar com
  // *ngFor e mudar a lista sem mexer no HTML.
  integrantes = [
    'Gabriel de Melo Guedes Souza',
    'Emanuelle Calheiros dos Santos Paula',
    'Hugo Prado de Azevedo Andrade',
  ];

  constructor(private auth: AuthService, private router: Router) {}

  sair(): void {
    this.auth.logout();
    this.router.navigateByUrl('/login', { replaceUrl: true });
  }
}
