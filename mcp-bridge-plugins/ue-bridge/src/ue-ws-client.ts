import WebSocket from 'ws';

export class UnrealWebSocketClient {
  private ws: WebSocket | null = null;
  private pendingRequests = new Map<number, { resolve: (val: any) => void; reject: (err: Error) => void }>();
  private messageIdCounter = 1;

  constructor(private url: string = 'ws://127.0.0.1:30020') {}

  public async connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);
      
      this.ws.on('open', () => {
        resolve();
      });

      this.ws.on('message', (data: WebSocket.RawData) => {
        try {
          const message = JSON.parse(data.toString());
          // Unreal Editor WebSocket sends back responses with a MessageId or RequestId (depending on version)
          const id = message.MessageId || message.RequestId;
          if (id && this.pendingRequests.has(id)) {
            this.pendingRequests.get(id)!.resolve(message);
            this.pendingRequests.delete(id);
          }
        } catch (err) {
          console.error('[UE Bridge] Websocket parse error', err);
        }
      });

      this.ws.on('error', (err) => {
        console.error('[UE Bridge] Websocket error', err);
        reject(err);
      });
      
      this.ws.on('close', () => {
        // Clears out pending
        for (const [_, handlers] of this.pendingRequests.entries()) {
          handlers.reject(new Error('WebSocket closed unexpectedly'));
        }
        this.pendingRequests.clear();
      });
    });
  }

  public async call(messageName: string, parameters: any = {}): Promise<any> {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error("Not connected to Unreal Engine WebSocket");
    }

    const id = this.messageIdCounter++;
    const payload = {
      MessageName: messageName,
      Parameters: parameters,
      MessageId: id
    };

    this.ws.send(JSON.stringify(payload));

    const timeoutMs = 30000;
    
    // Core Fix F-UE-04: NodeJS Memory Leak Guard with 30s Timeout
    return Promise.race([
      new Promise((resolve, reject) => {
        this.pendingRequests.set(id, { resolve, reject });
      }),
      new Promise((_, reject) => setTimeout(() => {
        if (this.pendingRequests.has(id)) {
          this.pendingRequests.delete(id);
          reject(new Error(`Timeout ${timeoutMs}ms waiting for Unreal Engine response to ${messageName}`));
        }
      }, timeoutMs))
    ]);
  }
}
