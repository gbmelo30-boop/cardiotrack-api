import { Component } from '@angular/core';
import { ToastController } from '@ionic/angular';

import { MedicoesService } from '../../core/medicoes.service';
import { Medicao } from '../../core/models';

@Component({
  selector: 'app-medicoes',
  standalone: false,
  templateUrl: './medicoes.page.html',
  styleUrls: ['./medicoes.page.scss'],
})
export class MedicoesPage {
  // Medição que está sendo preenchida no formulário.
  nova: Medicao = this.medicaoVazia();

  // Histórico carregado da API, exibido abaixo do formulário.
  historico: Medicao[] = [];
  carregando = false;

  constructor(
    private medicoes: MedicoesService,
    private toastCtrl: ToastController
  ) {}

  // ionViewWillEnter roda toda vez que a aba é aberta, garantindo a lista
  // sempre atualizada (inclusive depois de registrar em outra visita).
  ionViewWillEnter(): void {
    this.carregar();
  }

  registrar(): void {
    this.medicoes.registrar(this.nova).subscribe({
      next: async () => {
        await this.avisar('Medição registrada!', 'success');
        this.nova = this.medicaoVazia(); // limpa o formulário
        this.carregar();
      },
      error: async () => this.avisar('Não foi possível registrar.', 'danger'),
    });
  }

  private carregar(): void {
    this.carregando = true;
    this.medicoes.listar().subscribe({
      next: (lista) => {
        this.historico = lista;
        this.carregando = false;
      },
      error: () => (this.carregando = false),
    });
  }

  // Estado inicial de uma medição: sintomas desmarcados e valores em branco.
  private medicaoVazia(): Medicao {
    return {
      pressao_sistolica: undefined,
      pressao_diastolica: undefined,
      frequencia_cardiaca: undefined,
      oxigenacao_sangue: undefined,
      peso_corporal: undefined,
      falta_de_ar: false,
      dor_no_peito: false,
      tontura: false,
    };
  }

  private async avisar(mensagem: string, cor: string): Promise<void> {
    const toast = await this.toastCtrl.create({
      message: mensagem,
      duration: 2000,
      color: cor,
    });
    await toast.present();
  }
}
