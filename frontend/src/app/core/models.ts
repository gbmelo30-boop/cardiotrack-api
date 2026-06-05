// Tipos compartilhados por todo o app. Concentrar as interfaces aqui evita
// repetir a "forma" dos dados em cada arquivo e mantém o front alinhado ao
// contrato do back-end.

export interface Credenciais {
  email: string;
  senha: string;
}

// Espelha os campos que a tela de cadastro envia para a API.
export interface NovoUsuario {
  nome: string;
  sobrenome: string;
  email: string;
  telefone: string;
  senha: string;
  confirmar_senha: string;
  data_nascimento: string; // formato 'AAAA-MM-DD'
  sexo: string;
  pais_residencia: string;
}

export interface TokenResposta {
  token_acesso: string;
  tipo_token: string;
}

// Uma medição cardíaca. Quase tudo é opcional porque o usuário pode registrar
// só parte dos indicadores de cada vez.
export interface Medicao {
  id?: number;
  pressao_sistolica?: number | null;
  pressao_diastolica?: number | null;
  frequencia_cardiaca?: number | null;
  oxigenacao_sangue?: number | null;
  peso_corporal?: number | null;
  falta_de_ar: boolean;
  dor_no_peito: boolean;
  tontura: boolean;
  registrado_em?: string;
}

// Resumo entregue pelo back-end para alimentar os gráficos e o histórico.
export interface RelatorioSaude {
  total_registros: number;
  media_frequencia_cardiaca: number | null;
  media_pressao_sistolica: number | null;
  media_pressao_diastolica: number | null;
  media_oxigenacao: number | null;
  historico: Medicao[];
}
