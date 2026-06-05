import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { Medicao, RelatorioSaude } from './models';

// Conversa com os endpoints de medições do back-end. Repare que não há nada de
// token aqui: o cabeçalho de autenticação é adicionado automaticamente pelo
// interceptor, então este serviço só se preocupa com os dados.
@Injectable({ providedIn: 'root' })
export class MedicoesService {
  private readonly api = environment.apiUrl;

  constructor(private http: HttpClient) {}

  registrar(medicao: Medicao): Observable<Medicao> {
    return this.http.post<Medicao>(`${this.api}/medicoes`, medicao);
  }

  listar(): Observable<Medicao[]> {
    return this.http.get<Medicao[]>(`${this.api}/medicoes`);
  }

  obterRelatorio(): Observable<RelatorioSaude> {
    return this.http.get<RelatorioSaude>(`${this.api}/medicoes/relatorio`);
  }
}
