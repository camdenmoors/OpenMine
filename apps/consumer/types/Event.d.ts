export interface Event {
    _raw:           string;
    content:        string;
    hostname:       string;
    ip:             string;
    originating_id: string;
    path:           string;
    producer:       string;
    relationships:  string[];
    tags:           string[];
    type:           string;
    username:       string;
}
