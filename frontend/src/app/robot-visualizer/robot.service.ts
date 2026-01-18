import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { API_URL } from '../env';

export interface RobotStatus {
  robot_id?: number;
  is_parked: boolean;
  is_door_opened: boolean;
  is_reversing: boolean;
  is_charging: boolean;
  battery_status: number | string | null;
  message: string | null;
  led_rgb: [number, number, number] | null;
  packages: any[] | null;
  package_count?: number;
  package_count_large?: number;
  package_count_small?: number;
}

export interface RobotReadResponse {
  robot_id?: number;
  status?: RobotStatus;
  error?: string;
}

export interface CreateRobotParams {
  robot_id?: number;
  is_parked?: boolean;
  is_door_opened?: boolean;
  is_reversing?: boolean;
  is_charging?: boolean;
  battery_status?: number | string;
  message?: string;
  led_rgb?: [number, number, number] | string;
}

export interface CreateRobotResponse {
  robot_id?: number;
  status?: RobotStatus;
  robot_count?: number;
  error?: string;
}

@Injectable({ providedIn: 'root' })
export class RobotService {
  constructor(private http: HttpClient) {}

  getRobotStatus(robotId: number): Observable<RobotReadResponse> {
    return this.http
      .get<RobotReadResponse>(`${API_URL}/api/robot/read?robot_id=${robotId}`)
      .pipe(
        map((resp) => {
          if (!resp?.status) return resp;

          // Backend read endpoint nests the actual status inside resp.status.status
          const nestedStatus: any = (resp.status as any).status;
          const normalizedStatus: RobotStatus = nestedStatus && nestedStatus.robot_id !== undefined
            ? nestedStatus
            : (resp.status as RobotStatus);

          return { ...resp, status: normalizedStatus };
        })
      );
  }

  createRobot(params?: CreateRobotParams): Observable<CreateRobotResponse> {
    const normalized: Record<string, string> = {};

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value === undefined || value === null || value === '') {
          return;
        }

        if (typeof value === 'boolean') {
          normalized[key] = value ? 'true' : 'false';
          return;
        }

        if (Array.isArray(value)) {
          normalized[key] = value.join(',');
          return;
        }

        normalized[key] = String(value);
      });
    }

    const httpParams = new HttpParams({ fromObject: normalized });
    return this.http.post<CreateRobotResponse>(`${API_URL}/api/robot/create`, null, { params: httpParams });
  }
}
