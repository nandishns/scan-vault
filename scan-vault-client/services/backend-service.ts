const API_URL = "https://scan-vault.onrender.com";
const ACCESS_TOKEN = process.env.NEXT_PUBLIC_ACCESS_TOKEN ?? 'zamnnn';

if (!ACCESS_TOKEN) {
  console.error('Access token is not configured!');
}

export interface ScanResult {
  message: string;
  results: {
    file_name: string;
    sensitive_fields: any[];
  };
}

export class BackendService {
  private static getHeaders(includeContentType: boolean = false): HeadersInit {
    if (!ACCESS_TOKEN) {
      throw new Error('Access token is not configured. Please check your environment variables.');
    }

    const headers: HeadersInit = {
      'access_token': ACCESS_TOKEN
    };

    if (includeContentType) {
      headers['Content-Type'] = 'application/json';
    }

    return headers;
  }

  static async scanFile(file: File): Promise<ScanResult> {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/scan`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Scan API Error:', errorData);
        throw new Error(`Scan failed: ${JSON.stringify(errorData)}`);
      } 

      return await response.json();
    } catch (error) {
      console.error('Scan request failed:', error);
      throw error;
    }
  }

  static async saveResults(scanResult: any): Promise<void> {
    const response = await fetch(`${API_URL}/save-detection`, {
      method: 'POST',
      headers: this.getHeaders(true),
      body: JSON.stringify(scanResult),
    });

    if (!response.ok) {
      throw new Error('Failed to save results: ' + (await response.text()));
    }
  }

  static async fetchSavedResults(): Promise<any[]> {
    const response = await fetch(`${API_URL}/get-saved-detections`, {
      headers: this.getHeaders()
    });

    if (!response.ok) {
      throw new Error('Failed to fetch saved results: ' + (await response.text()));
    }

    const data = await response.json();
    return data[0]['detections'];
  }

  static async deleteResult(id: string): Promise<void> {
    const response = await fetch(`${API_URL}/delete-detection/${id}`, {
      method: 'DELETE',
      headers: this.getHeaders()
    });

    if (!response.ok) {
      throw new Error('Failed to delete result: ' + (await response.text()));
    }
  }

  static async pingServer(): Promise<boolean> {
    try {
      const response = await fetch(`${API_URL}/health`, {
        method: 'GET',
      });

      if (!response.ok) {
        console.warn('Server health check failed:', await response.text());
        return false;
      }

      return true;
    } catch (error) {
      console.error('Server ping failed:', error);
      return false;
    }
  }
}