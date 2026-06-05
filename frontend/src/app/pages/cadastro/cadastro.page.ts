import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { LoadingController, ToastController } from '@ionic/angular';

import { AuthService } from '../../core/auth.service';
import { NovoUsuario } from '../../core/models';

@Component({
  selector: 'app-cadastro',
  standalone: false,
  templateUrl: './cadastro.page.html',
  styleUrls: ['./cadastro.page.scss'],
})
export class CadastroPage {
  // Objeto único com todos os campos do formulário. Começa "zerado" e vai
  // sendo preenchido pelos inputs via ngModel.
  dados: NovoUsuario = {
    nome: '',
    sobrenome: '',
    email: '',
    telefone: '',
    senha: '',
    confirmar_senha: '',
    data_nascimento: '',
    sexo: '',
    pais_residencia: '',
  };

  constructor(
    private auth: AuthService,
    private router: Router,
    private loadingCtrl: LoadingController,
    private toastCtrl: ToastController
  ) {}

  async criarConta(): Promise<void> {
    // Confere as senhas já no app, antes de incomodar o servidor.
    if (this.dados.senha !== this.dados.confirmar_senha) {
      await this.avisar('As senhas não coincidem.', 'warning');
      return;
    }

    const carregando = await this.loadingCtrl.create({
      message: 'Criando conta...',
    });
    await carregando.present();

    this.auth.cadastrar(this.dados).subscribe({
      next: async () => {
        await carregando.dismiss();
        await this.avisar('Conta criada com sucesso! Faça login.', 'success');
        this.router.navigateByUrl('/login', { replaceUrl: true });
      },
      error: async (erro) => {
        await carregando.dismiss();
        // O back-end devolve 409 quando o e-mail já existe.
        const mensagem =
          erro?.status === 409
            ? 'Já existe uma conta com este e-mail.'
            : 'Não foi possível criar a conta. Verifique os dados.';
        await this.avisar(mensagem, 'danger');
      },
    });
  }

  private async avisar(mensagem: string, cor: string): Promise<void> {
    const toast = await this.toastCtrl.create({
      message: mensagem,
      duration: 2500,
      color: cor,
    });
    await toast.present();
  }
}
