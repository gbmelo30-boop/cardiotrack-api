// Configurações de ambiente para desenvolvimento.
//
// 'apiUrl' é o endereço onde o back-end (CardioTrack API) está rodando.
// - No navegador/emulador do próprio PC, 'localhost' funciona.
// - Ao gerar o APK e rodar num celular, troque por http://SEU_IP_LOCAL:8000
//   (ex.: http://192.168.0.12:8000), pois o celular não enxerga o 'localhost'
//   do computador. O IP da máquina aparece com 'ipconfig' no Windows.
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000',
};
