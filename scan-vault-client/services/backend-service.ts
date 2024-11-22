const API_URL = 'https://scan-vault.onrender.com';

export interface ScanResult {
  message: string;
  results: {
    file_name: string;
    sensitive_fields: {
      pii: Array<{
        type: string;
        value: string;
        confidence: string;
        context: string;
      }>;
      phi: Array<any>;
      pci: Array<any>;
    };
  };
}

export class BackendService {
  static async scanFile(file: File): Promise<ScanResult> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/scan`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Scan failed: ' + (await response.text()));
    }

    const data = await response.json();
    console.log('API Response:', data);
    return data;
  }

  static async saveResults(scanResult: ScanResult): Promise<void> {
    const response = await fetch(`${API_URL}/save`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(scanResult),
    });

    if (!response.ok) {
      throw new Error('Failed to save results: ' + (await response.text()));
    }
  }
}