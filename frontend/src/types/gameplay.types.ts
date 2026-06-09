export interface Chapter {

    id: number;

    title: string;

    description: string;

    user_id: number;
}

export interface Challenge {

    id: number;

    chapter_id: number;

    title: string;

    description: string;

    difficulty: string;
}

export interface SolvedChallenge {

    challenge_id: number;

    chapter_id: number;

    best_score: number;
}