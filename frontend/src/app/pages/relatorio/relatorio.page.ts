import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import Chart from 'chart.js/auto';

import { MedicoesService } from '../../core/medicoes.service';
import { RelatorioSaude } from '../../core/models';

@Component({
  selector: 'app-relatorio',
  standalone: false,
  templateUrl: './relatorio.page.html',
  styleUrls: ['./relatorio.page.scss'],
})
export class RelatorioPage implements AfterViewInit {
  // Referência ao <canvas> do template, onde o gráfico é desenhado.
  @ViewChild('grafico') private canvas!: ElementRef<HTMLCanvasElement>;

  relatorio: RelatorioSaude | null = null;
  private chart?: Chart;
  private prontoParaDesenhar = false;

  constructor(private medicoes: MedicoesService) {}

  ngAfterViewInit(): void {
    // Só depois que a view existe é que podemos desenhar no canvas.
    this.prontoParaDesenhar = true;
  }

  ionViewWillEnter(): void {
    this.carregar();
  }

  private carregar(): void {
    this.medicoes.obterRelatorio().subscribe((dados) => {
      this.relatorio = dados;
      if (this.prontoParaDesenhar) {
        this.desenharGrafico(dados);
      }
    });
  }

  // Monta um gráfico de linha com a evolução da frequência cardíaca ao longo
  // do tempo. O histórico vem do mais novo para o mais antigo, então invertemos
  // para o gráfico seguir a ordem cronológica.
  private desenharGrafico(dados: RelatorioSaude): void {
    const emOrdem = [...dados.historico].reverse();
    const rotulos = emOrdem.map((m) =>
      m.registrado_em ? new Date(m.registrado_em).toLocaleDateString('pt-BR') : ''
    );
    const frequencias = emOrdem.map((m) => m.frequencia_cardiaca ?? null);

    // Recria o gráfico do zero a cada carregamento para não acumular dados.
    this.chart?.destroy();
    this.chart = new Chart(this.canvas.nativeElement, {
      type: 'line',
      data: {
        labels: rotulos,
        datasets: [
          {
            label: 'Frequência cardíaca (bpm)',
            data: frequencias,
            borderColor: '#eb445a',
            backgroundColor: 'rgba(235, 68, 90, 0.2)',
            tension: 0.3,
            spanGaps: true,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: true } },
      },
    });
  }
}
