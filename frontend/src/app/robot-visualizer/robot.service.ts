import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from '../env';

export interface RobotStatus {
  is_parked: boolean;
  is_door_opened: boolean;
  is_reversing: boolean;
  is_charging: boolean;
  battery_status: number | string | null;
  message: string | null;
  led_rgb: [number, number, number] | null;
  packages: any[] | null;
}

export interface RobotReadResponse {
  robot_id?: number;
  status?: RobotStatus;
  error?: string;
}

export interface CreateRobotResponse {
  robot_id: number;
  status: any;
  robot_count: number;
}

@Injectable({ providedIn: 'root' })
export class RobotService {
  constructor(private http: HttpClient) {}

  getRobotStatus(robotId: number): Observable<RobotReadResponse> {
    return this.http.get<RobotReadResponse>(`${API_URL}/api/robot/read/${robotId}`);
  }

  createRobot(params?: Record<string, string | number | boolean | null | undefined>): Observable<CreateRobotResponse> {
    const query = params
      ? '?' + Object.entries(params)
          .filter(([, v]) => v !== undefined && v !== null && v !== '')
          .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
          .join('&')
      : '';
    return this.http.get<CreateRobotResponse>(`${API_URL}/api/robot/create${query}`);
  }
}
