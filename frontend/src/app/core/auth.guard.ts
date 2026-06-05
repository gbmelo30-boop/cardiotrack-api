import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';

import { AuthService } from './auth.service';

// "Porteiro" das rotas protegidas: se não houver token, manda o usuário de
// volta para a tela de login em vez de deixar abrir as telas internas.
@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private auth: AuthService, private router: Router) {}

  canActivate(): boolean | UrlTree {
    if (this.auth.estaAutenticado()) {
      return true;
    }
    return this.router.createUrlTree(['/login']);
  }
}
