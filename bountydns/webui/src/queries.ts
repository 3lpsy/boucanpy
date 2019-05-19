export interface IGeneralQS {
    page?: number;
    per_page?: number;
    sort_by?: string;
    sort_dir?: string;
    includes?: string[];
    search?: string;
}

export class GeneralQS implements IGeneralQS {
    page?: number = 1;
    per_page?: number = 20;
    sort_by?: string = 'id';
    sort_dir?: string = 'asc';
    includes?: string[] = [];
    search?: string = '';
}
