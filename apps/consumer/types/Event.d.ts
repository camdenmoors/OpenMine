export interface Event {
    // Meta: Raw payload of the generated event
    _raw:                       string;
    // Meta: Type of event (Message/Comment/Found Site)
    type:                       string;
    // Meta: Endpoint from which the event came from
    path:                       string;
    // Meta: Producer module name
    producer:                   string;
    // Meta: Hostname of source 
    hostname?:                  string;
    // Meta: IP address of source
    ip?:                        string;
    // Meta: UNIX Timestamp of when the event was created (i.e when a message was sent)
    time?:                      string;
    // Meta: UNIX Timestamp of when we found the event
    parse_time:                 Date;


    // UGC: ID of the creator of the event (including when the event is a user)
    user_id?:                   string;
    // UGC: Unique identifier provided by source platform (e.g Post ID, Message ID)
    originating_id:             string; 

    // UGC: Creator username
    username?:                  string;

    // UGC: Event content text
    content?:                   string;
    // UGC: IDs of associated users in event (Comment reply, message reply)
    relationships?:             string[];
    // UGC: Tags provided by user
    tags?:                      string[];

    // UGC: User's follower count
    "statistics.followers"?:    number;
    // UGC: Content view count
    "statistics.views"?:        number;
    // UGC: Content positive interactions
    "statistics.positive"?:     number;
    // UGC: Content negative interactions
    "statistics.negative"?:     number;
    // UGC: Content other interactions (e.g reply count)
    "statistics.interactions"?: number;
    // UGC: Content republish
    "statistics.republish"?:    number;
}
