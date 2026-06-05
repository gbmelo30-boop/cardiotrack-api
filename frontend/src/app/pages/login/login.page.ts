import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { LoadingController, ToastController } from '@ionic/angular';

import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-login',
  standalone: false,
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage {
  // Campos ligados aos inputs do formulário (two-way binding com ngModel).
  email = '';
  senha = '';

  constructor(
    private auth: AuthService,
    private router: Router,
    private loadingCtrl: LoadingController,
    private toastCtrl: ToastController
  ) {}

  async entrar(): Promise<void> {
    const carregando = await this.loadingCtrl.create({ message: 'Entrando...' });
    await carregando.present();

    this.auth.login({ email: this.email, senha: this.senha }).subscribe({
      next: async () => {
        await carregando.dismiss();
        // Limpa a pilha de navegação para o usuário não "voltar" ao login.
        this.router.navigateByUrl('/tabs', { replaceUrl: true });
      },
      error: async () => {
        await carregando.dismiss();
        await this.avisar('E-mail ou senha incorretos.');
      },
    });
  }

  private async avisar(mensagem: string): Promise<void> {
    const toast = await this.toastCtrl.create({
      message: mensagem,
      duration: 2500,
      color: 'danger',
    });
    await toast.present();
  }
}
