import { CapacitorConfig } from '@capacitor/cli';

// Configuração do Capacitor, a ponte que empacota o app web como aplicativo
// Android nativo (gerando o APK). 'webDir' aponta para a pasta que o
// "ng build" produz.
const config: CapacitorConfig = {
  appId: 'com.cardiotrack.app',
  appName: 'CardioTrack',
  webDir: 'www',
};

export default config;
