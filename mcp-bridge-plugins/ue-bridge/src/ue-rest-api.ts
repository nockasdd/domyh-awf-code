export class UnrealRestClient {
  constructor(private baseUrl: string = 'http://127.0.0.1:30010') {}

  private async request(endpoint: string, method: string, body?: unknown): Promise<any> {
    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      method,
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
      signal: AbortSignal.timeout(30_000),
    });
    if (!res.ok) {
      const text = await res.text().catch(() => res.statusText);
      throw new Error(`UE API ${res.status}: ${text}`);
    }
    return res.json();
  }

  // ── Existing ─────────────────────────────────────────────

  public async getInfo(): Promise<any> {
    return this.request('/remote/info', 'GET');
  }

  public async describeObject(objectPath: string): Promise<any> {
    return this.request('/remote/object/describe', 'PUT', { ObjectPath: objectPath });
  }

  public async searchAssets(query: string, filterClass?: string): Promise<any> {
    const payload: any = { Query: query };
    if (filterClass) payload.Filter = { ClassNames: [filterClass] };
    return this.request('/remote/search/assets', 'PUT', payload);
  }

  public async setProperty(objectPath: string, propertyName: string, propertyValue: any): Promise<any> {
    return this.request('/remote/object/property', 'PUT', {
      ObjectPath: objectPath,
      PropertyName: propertyName,
      PropertyValue: propertyValue,
    });
  }

  // ── Phase 1 — NEW ────────────────────────────────────────

  /**
   * Call any Blueprint-callable UFunction on a UObject.
   * This is the most powerful endpoint — can spawn actors, call BP functions, etc.
   */
  public async callFunction(objectPath: string, functionName: string, params: Record<string, unknown> = {}): Promise<any> {
    return this.request('/remote/object/call', 'PUT', {
      ObjectPath: objectPath,
      FunctionName: functionName,
      Parameters: params,
      GenerateTransaction: true,
    });
  }

  /**
   * Get a property value from a UObject.
   */
  public async getProperty(objectPath: string, propertyName: string): Promise<any> {
    return this.request('/remote/object/property', 'PUT', {
      ObjectPath: objectPath,
      PropertyName: propertyName,
      Access: 'READ_ACCESS',
    });
  }

  /**
   * Batch multiple remote calls in a single HTTP request.
   */
  public async batch(requests: Array<{ objectPath: string; functionName: string; params?: Record<string, unknown> }>): Promise<any> {
    const body = {
      Requests: requests.map((r, i) => ({
        RequestId: i,
        URL: '/remote/object/call',
        Verb: 'PUT',
        Body: {
          ObjectPath: r.objectPath,
          FunctionName: r.functionName,
          Parameters: r.params ?? {},
        },
      })),
    };
    return this.request('/remote/batch', 'PUT', body);
  }
}
