import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

import { environment } from '../../environments/environment';
import { Credenciais, NovoUsuario, TokenResposta } from './models';

// Cuida de tudo relacionado a "quem é o usuário": cadastro, login, logout e o
// armazenamento do token. Por ser providedIn: 'root', existe uma única
// instância compartilhada em todo o app.
@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly api = environment.apiUrl;
  // Chave usada para guardar o token no navegador entre as sessões.
  private readonly chaveToken = 'cardiotrack_token';

  constructor(private http: HttpClient) {}

  cadastrar(dados: NovoUsuario): Observable<unknown> {
    return this.http.post(`${this.api}/usuarios`, dados);
  }

  // Faz o login e, ao receber o token, já o guarda para as próximas requisições.
  login(credenciais: Credenciais): Observable<TokenResposta> {
    return this.http
      .post<TokenResposta>(`${this.api}/auth/login`, credenciais)
      .pipe(tap((resposta) => this.guardarToken(resposta.token_acesso)));
  }

  logout(): void {
    localStorage.removeItem(this.chaveToken);
  }

  obterToken(): string | null {
    return localStorage.getItem(this.chaveToken);
  }

  estaAutenticado(): boolean {
    return this.obterToken() !== null;
  }

  private guardarToken(token: string): void {
    localStorage.setItem(this.chaveToken, token);
  }
}
