import { User } from './user.model';

export declare class Game {
  id: string;
  created_at: string;
  updated_at: string;
  description: string;
  gender: 'M' | 'F' | null;
  owner: User;
}
