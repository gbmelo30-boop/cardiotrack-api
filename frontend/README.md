# CardioTrack — App (Front-end)

Aplicativo mobile do **CardioTrack**, feito em **Ionic + Angular**, que consome a
[CardioTrack API](../) (back-end). Permite criar conta, fazer login, registrar
medições cardíacas e visualizar relatórios com gráficos.

## Telas

- **Login** e **Criar Conta**
- **Acompanhamento** — registro de medições (pressão, frequência, oxigenação,
  peso e sintomas) e histórico
- **Relatório** — médias e gráfico de evolução
- **Integrantes** — tela com os nomes do grupo

## Organização do código

```
src/app/
├── core/          # serviços, guard e interceptor (a "regra" do app)
│   ├── auth.service.ts        # cadastro, login e token
│   ├── medicoes.service.ts    # chamadas das medições
│   ├── token.interceptor.ts   # anexa o token JWT em cada requisição
│   ├── auth.guard.ts          # protege as telas internas
│   └── models.ts              # tipos compartilhados
└── pages/         # uma pasta por tela (componentização)
    ├── login/  cadastro/  tabs/
    └── medicoes/  relatorio/  integrantes/
```

As chamadas à API ficam centralizadas nos *services* dentro de `core/`. As telas
(em `pages/`) só pedem os dados ao serviço e cuidam da interface — nenhuma tela
fala HTTP diretamente.

## Como executar (navegador)

```bash
npm install
npm start        # ou: ionic serve
```

Abra `http://localhost:8100`. O back-end precisa estar rodando (veja o README do
back-end). O endereço da API é configurado em `src/environments/environment.ts`.

## Apontando para o back-end

- **No navegador do PC:** `apiUrl` pode ficar como `http://localhost:8000`.
- **No celular (APK):** o aparelho não enxerga o `localhost` do computador.
  Descubra o IP da sua máquina na rede (`ipconfig` no Windows) e ajuste
  `src/environments/environment.ts` para algo como `http://192.168.0.12:8000`.
  O computador e o celular precisam estar na mesma rede Wi-Fi.

## Gerando o APK (Android)

Requer Android Studio instalado.

```bash
npm install
npm run build                 # gera a pasta www
npx cap add android           # cria a pasta android/ (só na primeira vez)
npx cap sync                  # copia o app web para o projeto Android
npx cap open android          # abre no Android Studio
```

No Android Studio: **Build > Build Bundle(s)/APK(s) > Build APK(s)**. O APK
gerado fica em `android/app/build/outputs/apk/`.
