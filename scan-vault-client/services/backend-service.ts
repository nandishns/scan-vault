// const API_URL = 'https://scan-vault.onrender.com';
const API_URL = 'http://localhost:8000';

export interface ScanResult {
  message: string;
  results: {
    file_name: string;
    sensitive_fields: any[];
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

  static async saveResults(scanResult: any): Promise<void> {
    console.log('Saving results:', scanResult);
    const response = await fetch(`${API_URL}/save-detection`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(scanResult),
    });
    console.log('Response:', response);
    if (!response.ok) {
      throw new Error('Failed to save results: ' + (await response.text()));
    }
  }

  static async fetchSavedResults(): Promise<any[]> {
    const response = await fetch(`${API_URL}/get-saved-detections`);
    if (!response.ok) {
      throw new Error('Failed to fetch saved results: ' + (await response.text()));
    }
    const data = await response.json();
    console.log('data:', data[0]['detections'])
    
    return data[0]['detections'];
  }

  static async deleteResult(id: number): Promise<void> {
    const response = await fetch(`${API_URL}/delete-detection/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete result: ' + (await response.text()));
    }
  }
}