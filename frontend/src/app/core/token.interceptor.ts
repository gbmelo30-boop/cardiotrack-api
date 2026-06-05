import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Observable } from 'rxjs';

import { AuthService } from './auth.service';

// Intercepta toda requisição que sai do app e, se houver um token guardado,
// anexa o cabeçalho "Authorization: Bearer <token>". Assim nenhuma tela precisa
// lembrar de enviar o token manualmente - fica tudo num lugar só.
@Injectable()
export class TokenInterceptor implements HttpInterceptor {
  constructor(private auth: AuthService) {}

  intercept(
    requisicao: HttpRequest<unknown>,
    proximo: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    const token = this.auth.obterToken();

    if (token) {
      const comToken = requisicao.clone({
        setHeaders: { Authorization: `Bearer ${token}` },
      });
      return proximo.handle(comToken);
    }

    return proximo.handle(requisicao);
  }
}
