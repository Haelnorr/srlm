-- Database: celery

-- DROP DATABASE IF EXISTS celery;

CREATE DATABASE celery
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

\connect celery

-- SCHEMA: celery

-- DROP SCHEMA IF EXISTS celery ;

CREATE SCHEMA IF NOT EXISTS celery
    AUTHORIZATION postgres;

-- SEQUENCE: celery.celery_taskmeta_id_seq

-- DROP SEQUENCE IF EXISTS celery.celery_taskmeta_id_seq;

CREATE SEQUENCE IF NOT EXISTS celery.celery_taskmeta_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

-- SEQUENCE: celery.celery_tasksetmeta_id_seq

-- DROP SEQUENCE IF EXISTS celery.celery_tasksetmeta_id_seq;

CREATE SEQUENCE IF NOT EXISTS celery.celery_tasksetmeta_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;


-- Table: celery.celery_taskmeta

-- DROP TABLE IF EXISTS celery.celery_taskmeta;

CREATE TABLE IF NOT EXISTS celery.celery_taskmeta
(
    id bigint NOT NULL DEFAULT nextval('celery.celery_taskmeta_id_seq'::regclass),
    task_id character varying(155) COLLATE pg_catalog."default",
    status character varying(50) COLLATE pg_catalog."default",
    result bytea,
    date_done timestamp with time zone,
    traceback text COLLATE pg_catalog."default",
    name character varying(155) COLLATE pg_catalog."default",
    args bytea,
    kwargs bytea,
    worker character varying(155) COLLATE pg_catalog."default",
    retries bigint,
    queue character varying(155) COLLATE pg_catalog."default",
    CONSTRAINT idx_41641_primary PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS celery.celery_taskmeta
    OWNER to postgres;
-- Index: idx_41641_task_id

-- DROP INDEX IF EXISTS celery.idx_41641_task_id;

CREATE UNIQUE INDEX IF NOT EXISTS idx_41641_task_id
    ON celery.celery_taskmeta USING btree
    (task_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: celery.celery_tasksetmeta

-- DROP TABLE IF EXISTS celery.celery_tasksetmeta;

CREATE TABLE IF NOT EXISTS celery.celery_tasksetmeta
(
    id bigint NOT NULL DEFAULT nextval('celery.celery_tasksetmeta_id_seq'::regclass),
    taskset_id character varying(155) COLLATE pg_catalog."default",
    result bytea,
    date_done timestamp with time zone,
    CONSTRAINT idx_41648_primary PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS celery.celery_tasksetmeta
    OWNER to postgres;
-- Index: idx_41648_taskset_id

-- DROP INDEX IF EXISTS celery.idx_41648_taskset_id;

CREATE UNIQUE INDEX IF NOT EXISTS idx_41648_taskset_id
    ON celery.celery_tasksetmeta USING btree
    (taskset_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

ALTER SEQUENCE celery.celery_taskmeta_id_seq
    OWNED BY celery.celery_taskmeta.id;

ALTER SEQUENCE celery.celery_taskmeta_id_seq
    OWNER TO postgres;

ALTER SEQUENCE celery.celery_tasksetmeta_id_seq
    OWNED BY celery.celery_tasksetmeta.id;

ALTER SEQUENCE celery.celery_tasksetmeta_id_seq
    OWNER TO postgres;


-- Database: league_manager_api

-- DROP DATABASE IF EXISTS league_manager_api;

CREATE DATABASE league_manager_api
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;



\connect league_manager_api

-- SCHEMA: api_access

-- DROP SCHEMA IF EXISTS api_access ;

CREATE SCHEMA IF NOT EXISTS api_access
    AUTHORIZATION postgres;


-- SCHEMA: league_manager

-- DROP SCHEMA IF EXISTS league_manager ;

CREATE SCHEMA IF NOT EXISTS league_manager
    AUTHORIZATION postgres;


-- Table: public.alembic_version

-- DROP TABLE IF EXISTS public.alembic_version;

CREATE TABLE IF NOT EXISTS public.alembic_version
(
    version_num character varying(32) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.alembic_version
    OWNER to postgres;


INSERT INTO public.alembic_version(
	version_num)
	VALUES ('ee7faff8156e');


-- SEQUENCE: api_access.authorized_app_id_seq

-- DROP SEQUENCE IF EXISTS api_access.authorized_app_id_seq;

CREATE SEQUENCE IF NOT EXISTS api_access.authorized_app_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;



-- Table: api_access.authorized_app

-- DROP TABLE IF EXISTS api_access.authorized_app;

CREATE TABLE IF NOT EXISTS api_access.authorized_app
(
    id integer NOT NULL DEFAULT nextval('api_access.authorized_app_id_seq'::regclass),
    name character varying(32) COLLATE pg_catalog."default",
    token character varying(34) COLLATE pg_catalog."default",
    token_expiration timestamp without time zone NOT NULL,
    CONSTRAINT authorized_app_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS api_access.authorized_app
    OWNER to postgres;
-- Index: ix_api_access_authorized_app_name

-- DROP INDEX IF EXISTS api_access.ix_api_access_authorized_app_name;

CREATE UNIQUE INDEX IF NOT EXISTS ix_api_access_authorized_app_name
    ON api_access.authorized_app USING btree
    (name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_api_access_authorized_app_token

-- DROP INDEX IF EXISTS api_access.ix_api_access_authorized_app_token;

CREATE UNIQUE INDEX IF NOT EXISTS ix_api_access_authorized_app_token
    ON api_access.authorized_app USING btree
    (token COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

INSERT INTO api_access.authorized_app(
	id, name, token, token_expiration)
	VALUES (1, 'Dev', '6001d967e76181e8eb3d61f100bd17f653', '2026-04-24 14:21:59');

ALTER SEQUENCE api_access.authorized_app_id_seq
    OWNED BY api_access.authorized_app.id;

ALTER SEQUENCE api_access.authorized_app_id_seq
    OWNER TO postgres;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 207 (class 1259 OID 20717)
-- Name: arena; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.arena (
    value character varying(32) NOT NULL,
    label character varying(32) NOT NULL,
    info character varying(64)
);


ALTER TABLE league_manager.arena OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 20726)
-- Name: award; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.award (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    description character varying(128) NOT NULL
);


ALTER TABLE league_manager.award OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 20724)
-- Name: award_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.award_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.award_id_seq OWNER TO postgres;

--
-- TOC entry 3449 (class 0 OID 0)
-- Dependencies: 208
-- Name: award_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.award_id_seq OWNED BY league_manager.award.id;


--
-- TOC entry 220 (class 1259 OID 20786)
-- Name: discord; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.discord (
    id integer NOT NULL,
    discord_id character varying(32) NOT NULL,
    user_id integer,
    access_token character varying(64),
    refresh_token character varying(64),
    token_expiration timestamp without time zone
);


ALTER TABLE league_manager.discord OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 20784)
-- Name: discord_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.discord_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.discord_id_seq OWNER TO postgres;

--
-- TOC entry 3450 (class 0 OID 0)
-- Dependencies: 219
-- Name: discord_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.discord_id_seq OWNED BY league_manager.discord.id;


--
-- TOC entry 232 (class 1259 OID 20883)
-- Name: division; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.division (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    league_id integer NOT NULL,
    acronym character varying(5) NOT NULL,
    description character varying(128)
);


ALTER TABLE league_manager.division OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 20881)
-- Name: division_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.division_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.division_id_seq OWNER TO postgres;

--
-- TOC entry 3451 (class 0 OID 0)
-- Dependencies: 231
-- Name: division_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.division_id_seq OWNED BY league_manager.division.id;


--
-- TOC entry 210 (class 1259 OID 20733)
-- Name: end_reason; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.end_reason (
    value character varying(32) NOT NULL,
    label character varying(32) NOT NULL,
    info character varying(64)
);


ALTER TABLE league_manager.end_reason OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 20800)
-- Name: event; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.event (
    id integer NOT NULL,
    "timestamp" timestamp without time zone,
    user_id integer,
    module character varying(50),
    message character varying(200)
);


ALTER TABLE league_manager.event OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 20798)
-- Name: event_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.event_id_seq OWNER TO postgres;

--
-- TOC entry 3452 (class 0 OID 0)
-- Dependencies: 221
-- Name: event_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.event_id_seq OWNED BY league_manager.event.id;


--
-- TOC entry 238 (class 1259 OID 20933)
-- Name: final; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.final (
    id integer NOT NULL,
    season_division_id integer,
    best_of integer NOT NULL,
    elimination boolean NOT NULL,
    round character varying(20) NOT NULL,
    home_team_id integer,
    away_team_id integer,
    completed boolean NOT NULL
);


ALTER TABLE league_manager.final OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 20931)
-- Name: final_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.final_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.final_id_seq OWNER TO postgres;

--
-- TOC entry 3453 (class 0 OID 0)
-- Dependencies: 237
-- Name: final_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.final_id_seq OWNED BY league_manager.final.id;


--
-- TOC entry 246 (class 1259 OID 21017)
-- Name: final_results; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.final_results (
    id integer NOT NULL,
    final_id integer,
    winner_id integer,
    loser_id integer,
    home_team_score integer NOT NULL,
    away_team_score integer NOT NULL
);


ALTER TABLE league_manager.final_results OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 21015)
-- Name: final_results_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.final_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.final_results_id_seq OWNER TO postgres;

--
-- TOC entry 3454 (class 0 OID 0)
-- Dependencies: 245
-- Name: final_results_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.final_results_id_seq OWNED BY league_manager.final_results.id;


--
-- TOC entry 248 (class 1259 OID 21040)
-- Name: free_agent; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.free_agent (
    id integer NOT NULL,
    player_id integer,
    season_division_id integer,
    start_date timestamp without time zone,
    end_date timestamp without time zone
);


ALTER TABLE league_manager.free_agent OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 21038)
-- Name: free_agent_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.free_agent_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.free_agent_id_seq OWNER TO postgres;

--
-- TOC entry 3455 (class 0 OID 0)
-- Dependencies: 247
-- Name: free_agent_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.free_agent_id_seq OWNED BY league_manager.free_agent.id;


--
-- TOC entry 211 (class 1259 OID 20740)
-- Name: game_mode; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.game_mode (
    value character varying(32) NOT NULL,
    label character varying(32) NOT NULL,
    info character varying(64)
);


ALTER TABLE league_manager.game_mode OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 20815)
-- Name: league; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.league (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    acronym character varying(5) NOT NULL,
    server_region_value character varying(32)
);


ALTER TABLE league_manager.league OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 20813)
-- Name: league_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.league_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.league_id_seq OWNER TO postgres;

--
-- TOC entry 3456 (class 0 OID 0)
-- Dependencies: 223
-- Name: league_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.league_id_seq OWNED BY league_manager.league.id;


--
-- TOC entry 260 (class 1259 OID 21183)
-- Name: lobby; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.lobby (
    id integer NOT NULL,
    match_id integer,
    lobby_id character varying(64) NOT NULL,
    active boolean NOT NULL,
    password character varying(64) NOT NULL,
    task_id character varying(64)
);


ALTER TABLE league_manager.lobby OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 21181)
-- Name: lobby_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.lobby_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.lobby_id_seq OWNER TO postgres;

--
-- TOC entry 3457 (class 0 OID 0)
-- Dependencies: 259
-- Name: lobby_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.lobby_id_seq OWNED BY league_manager.lobby.id;


--
-- TOC entry 250 (class 1259 OID 21058)
-- Name: match; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.match (
    id integer NOT NULL,
    season_division_id integer,
    home_team_id integer,
    away_team_id integer,
    round integer,
    match_week integer,
    cancelled character varying(32),
    streamer_id integer,
    final_id integer
);


ALTER TABLE league_manager.match OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 21196)
-- Name: match_availability; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.match_availability (
    id integer NOT NULL,
    match_id integer,
    team_id integer,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    available boolean NOT NULL
);


ALTER TABLE league_manager.match_availability OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 21194)
-- Name: match_availability_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.match_availability_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.match_availability_id_seq OWNER TO postgres;

--
-- TOC entry 3458 (class 0 OID 0)
-- Dependencies: 261
-- Name: match_availability_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.match_availability_id_seq OWNED BY league_manager.match_availability.id;


--
-- TOC entry 269 (class 1259 OID 21268)
-- Name: match_data; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.match_data (
    id integer NOT NULL,
    lobby_id integer,
    processed boolean NOT NULL,
    accepted boolean NOT NULL,
    match_id character varying(64) NOT NULL,
    region character varying(16) NOT NULL,
    gamemode character varying(16) NOT NULL,
    created timestamp without time zone NOT NULL,
    arena character varying(16) NOT NULL,
    home_score integer NOT NULL,
    away_score integer NOT NULL,
    winner character varying(10) NOT NULL,
    current_period integer NOT NULL,
    periods_enabled boolean NOT NULL,
    custom_mercy_rule character varying(16) NOT NULL,
    end_reason character varying(32) NOT NULL,
    source character varying(10)
);


ALTER TABLE league_manager.match_data OWNER TO postgres;

--
-- TOC entry 268 (class 1259 OID 21266)
-- Name: match_data_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.match_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.match_data_id_seq OWNER TO postgres;

--
-- TOC entry 3459 (class 0 OID 0)
-- Dependencies: 268
-- Name: match_data_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.match_data_id_seq OWNED BY league_manager.match_data.id;


--
-- TOC entry 249 (class 1259 OID 21056)
-- Name: match_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.match_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.match_id_seq OWNER TO postgres;

--
-- TOC entry 3460 (class 0 OID 0)
-- Dependencies: 249
-- Name: match_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.match_id_seq OWNED BY league_manager.match.id;


--
-- TOC entry 263 (class 1259 OID 21212)
-- Name: match_result; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.match_result (
    id integer NOT NULL,
    winner_id integer,
    loser_id integer,
    draw boolean,
    score_winner integer NOT NULL,
    score_loser integer NOT NULL,
    overtime boolean NOT NULL,
    forfeit boolean NOT NULL,
    vod character varying(128),
    completed_date timestamp without time zone
);


ALTER TABLE league_manager.match_result OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 21234)
-- Name: match_review; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.match_review (
    id integer NOT NULL,
    match_id integer,
    type character varying(16) NOT NULL,
    reason character varying(256) NOT NULL,
    raised_by character varying(32),
    comments character varying(256),
    resolved boolean NOT NULL,
    resolved_by integer,
    resolved_on integer
);


ALTER TABLE league_manager.match_review OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 21232)
-- Name: match_review_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.match_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.match_review_id_seq OWNER TO postgres;

--
-- TOC entry 3461 (class 0 OID 0)
-- Dependencies: 264
-- Name: match_review_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.match_review_id_seq OWNED BY league_manager.match_review.id;


--
-- TOC entry 267 (class 1259 OID 21255)
-- Name: match_schedule; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.match_schedule (
    id integer NOT NULL,
    match_id integer,
    scheduled_time timestamp without time zone,
    home_team_accepted boolean NOT NULL,
    away_team_accepted boolean NOT NULL
);


ALTER TABLE league_manager.match_schedule OWNER TO postgres;

--
-- TOC entry 266 (class 1259 OID 21253)
-- Name: match_schedule_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.match_schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.match_schedule_id_seq OWNER TO postgres;

--
-- TOC entry 3462 (class 0 OID 0)
-- Dependencies: 266
-- Name: match_schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.match_schedule_id_seq OWNED BY league_manager.match_schedule.id;


--
-- TOC entry 226 (class 1259 OID 20831)
-- Name: matchtype; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.matchtype (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    description character varying(128),
    periods boolean NOT NULL,
    arena character varying(32) NOT NULL,
    mercy_rule integer NOT NULL,
    match_length integer NOT NULL,
    game_mode character varying(32) NOT NULL,
    num_players integer NOT NULL
);


ALTER TABLE league_manager.matchtype OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 20829)
-- Name: matchtype_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.matchtype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.matchtype_id_seq OWNER TO postgres;

--
-- TOC entry 3463 (class 0 OID 0)
-- Dependencies: 225
-- Name: matchtype_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.matchtype_id_seq OWNED BY league_manager.matchtype.id;


--
-- TOC entry 213 (class 1259 OID 20749)
-- Name: permission; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.permission (
    id integer NOT NULL,
    key character varying(32) NOT NULL,
    description character varying(128)
);


ALTER TABLE league_manager.permission OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 20747)
-- Name: permission_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.permission_id_seq OWNER TO postgres;

--
-- TOC entry 3464 (class 0 OID 0)
-- Dependencies: 212
-- Name: permission_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.permission_id_seq OWNED BY league_manager.permission.id;


--
-- TOC entry 240 (class 1259 OID 20956)
-- Name: player; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.player (
    id integer NOT NULL,
    slap_id integer,
    user_id integer,
    player_name character varying(64) NOT NULL,
    rookie boolean NOT NULL,
    first_season_id integer,
    next_name_change timestamp without time zone
);


ALTER TABLE league_manager.player OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 21091)
-- Name: player_award; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.player_award (
    id integer NOT NULL,
    player_id integer,
    award_id integer,
    season_division_id integer
);


ALTER TABLE league_manager.player_award OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 21089)
-- Name: player_award_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.player_award_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.player_award_id_seq OWNER TO postgres;

--
-- TOC entry 3465 (class 0 OID 0)
-- Dependencies: 251
-- Name: player_award_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.player_award_id_seq OWNED BY league_manager.player_award.id;


--
-- TOC entry 239 (class 1259 OID 20954)
-- Name: player_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.player_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.player_id_seq OWNER TO postgres;

--
-- TOC entry 3466 (class 0 OID 0)
-- Dependencies: 239
-- Name: player_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.player_id_seq OWNED BY league_manager.player.id;


--
-- TOC entry 271 (class 1259 OID 21281)
-- Name: player_match_data; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.player_match_data (
    id integer NOT NULL,
    match_id integer,
    player_id integer,
    team_id integer,
    goals integer,
    shots integer,
    assists integer,
    saves integer,
    primary_assists integer,
    secondary_assists integer,
    passes integer,
    blocks integer,
    takeaways integer,
    turnovers integer,
    possession_time_sec integer,
    game_winning_goals integer,
    overtime_goals integer,
    post_hits integer,
    faceoffs_won integer,
    faceoffs_lost integer,
    score integer,
    current_period integer NOT NULL,
    stat_total boolean NOT NULL
);


ALTER TABLE league_manager.player_match_data OWNER TO postgres;

--
-- TOC entry 270 (class 1259 OID 21279)
-- Name: player_match_data_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.player_match_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.player_match_data_id_seq OWNER TO postgres;

--
-- TOC entry 3467 (class 0 OID 0)
-- Dependencies: 270
-- Name: player_match_data_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.player_match_data_id_seq OWNED BY league_manager.player_match_data.id;


--
-- TOC entry 254 (class 1259 OID 21114)
-- Name: player_team; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.player_team (
    id integer NOT NULL,
    player_id integer,
    team_id integer,
    start_date timestamp without time zone,
    end_date timestamp without time zone
);


ALTER TABLE league_manager.player_team OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 21112)
-- Name: player_team_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.player_team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.player_team_id_seq OWNER TO postgres;

--
-- TOC entry 3468 (class 0 OID 0)
-- Dependencies: 253
-- Name: player_team_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.player_team_id_seq OWNED BY league_manager.player_team.id;


--
-- TOC entry 234 (class 1259 OID 20896)
-- Name: season; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.season (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    acronym character varying(5) NOT NULL,
    league_id integer NOT NULL,
    start_date date,
    end_date date,
    finals_start date,
    finals_end date,
    match_type_id integer,
    can_register boolean
);


ALTER TABLE league_manager.season OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 20915)
-- Name: season_division; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.season_division (
    id integer NOT NULL,
    season_id integer,
    division_id integer
);


ALTER TABLE league_manager.season_division OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 20913)
-- Name: season_division_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.season_division_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.season_division_id_seq OWNER TO postgres;

--
-- TOC entry 3469 (class 0 OID 0)
-- Dependencies: 235
-- Name: season_division_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.season_division_id_seq OWNED BY league_manager.season_division.id;


--
-- TOC entry 242 (class 1259 OID 20976)
-- Name: season_division_team; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.season_division_team (
    id integer NOT NULL,
    season_division_id integer,
    team_id integer
);


ALTER TABLE league_manager.season_division_team OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 20974)
-- Name: season_division_team_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.season_division_team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.season_division_team_id_seq OWNER TO postgres;

--
-- TOC entry 3470 (class 0 OID 0)
-- Dependencies: 241
-- Name: season_division_team_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.season_division_team_id_seq OWNED BY league_manager.season_division_team.id;


--
-- TOC entry 233 (class 1259 OID 20894)
-- Name: season_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.season_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.season_id_seq OWNER TO postgres;

--
-- TOC entry 3471 (class 0 OID 0)
-- Dependencies: 233
-- Name: season_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.season_id_seq OWNED BY league_manager.season.id;


--
-- TOC entry 256 (class 1259 OID 21132)
-- Name: season_registration; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.season_registration (
    id integer NOT NULL,
    team_id integer,
    player_id integer,
    season_id integer NOT NULL,
    division_id integer,
    status character varying(16) NOT NULL,
    type character varying(10) NOT NULL
);


ALTER TABLE league_manager.season_registration OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 21130)
-- Name: season_registration_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.season_registration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.season_registration_id_seq OWNER TO postgres;

--
-- TOC entry 3472 (class 0 OID 0)
-- Dependencies: 255
-- Name: season_registration_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.season_registration_id_seq OWNED BY league_manager.season_registration.id;


--
-- TOC entry 214 (class 1259 OID 20756)
-- Name: server_region; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.server_region (
    value character varying(32) NOT NULL,
    label character varying(32) NOT NULL,
    info character varying(64),
    utc_offset character varying(7)
);


ALTER TABLE league_manager.server_region OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 20765)
-- Name: team; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.team (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    acronym character varying(5) NOT NULL,
    color character varying(7),
    logo character varying(128),
    founded_date timestamp without time zone
);


ALTER TABLE league_manager.team OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 20994)
-- Name: team_award; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.team_award (
    id integer NOT NULL,
    team_id integer,
    award_id integer,
    season_division_id integer
);


ALTER TABLE league_manager.team_award OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 20992)
-- Name: team_award_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.team_award_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.team_award_id_seq OWNER TO postgres;

--
-- TOC entry 3473 (class 0 OID 0)
-- Dependencies: 243
-- Name: team_award_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.team_award_id_seq OWNED BY league_manager.team_award.id;


--
-- TOC entry 215 (class 1259 OID 20763)
-- Name: team_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.team_id_seq OWNER TO postgres;

--
-- TOC entry 3474 (class 0 OID 0)
-- Dependencies: 215
-- Name: team_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.team_id_seq OWNED BY league_manager.team.id;


--
-- TOC entry 258 (class 1259 OID 21160)
-- Name: team_invites; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.team_invites (
    id integer NOT NULL,
    team_id integer NOT NULL,
    invited_player_id integer NOT NULL,
    inviting_player_id integer NOT NULL,
    status character varying(16) NOT NULL
);


ALTER TABLE league_manager.team_invites OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 21158)
-- Name: team_invites_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.team_invites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.team_invites_id_seq OWNER TO postgres;

--
-- TOC entry 3475 (class 0 OID 0)
-- Dependencies: 257
-- Name: team_invites_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.team_invites_id_seq OWNED BY league_manager.team_invites.id;


--
-- TOC entry 228 (class 1259 OID 20851)
-- Name: twitch; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.twitch (
    id integer NOT NULL,
    twitch_id character varying(32) NOT NULL,
    user_id integer NOT NULL,
    access_token character varying(64) NOT NULL,
    refresh_token character varying(64) NOT NULL,
    token_expiration timestamp without time zone NOT NULL
);


ALTER TABLE league_manager.twitch OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 20849)
-- Name: twitch_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.twitch_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.twitch_id_seq OWNER TO postgres;

--
-- TOC entry 3476 (class 0 OID 0)
-- Dependencies: 227
-- Name: twitch_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.twitch_id_seq OWNED BY league_manager.twitch.id;


--
-- TOC entry 218 (class 1259 OID 20775)
-- Name: user; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager."user" (
    id integer NOT NULL,
    username character varying(64) NOT NULL,
    email character varying(120),
    password_hash character varying(128),
    reset_pass boolean NOT NULL,
    token character varying(32),
    token_expiration timestamp without time zone,
    steam_id character varying(32)
);


ALTER TABLE league_manager."user" OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 20773)
-- Name: user_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.user_id_seq OWNER TO postgres;

--
-- TOC entry 3477 (class 0 OID 0)
-- Dependencies: 217
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.user_id_seq OWNED BY league_manager."user".id;


--
-- TOC entry 230 (class 1259 OID 20865)
-- Name: user_permissions; Type: TABLE; Schema: league_manager; Owner: postgres
--

CREATE TABLE league_manager.user_permissions (
    id integer NOT NULL,
    user_id integer,
    permission_id integer,
    additional_modifiers character varying(128)
);


ALTER TABLE league_manager.user_permissions OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 20863)
-- Name: user_permissions_id_seq; Type: SEQUENCE; Schema: league_manager; Owner: postgres
--

CREATE SEQUENCE league_manager.user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE league_manager.user_permissions_id_seq OWNER TO postgres;

--
-- TOC entry 3478 (class 0 OID 0)
-- Dependencies: 229
-- Name: user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: league_manager; Owner: postgres
--

ALTER SEQUENCE league_manager.user_permissions_id_seq OWNED BY league_manager.user_permissions.id;


--
-- TOC entry 3064 (class 2604 OID 20729)
-- Name: award id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.award ALTER COLUMN id SET DEFAULT nextval('league_manager.award_id_seq'::regclass);


--
-- TOC entry 3068 (class 2604 OID 20789)
-- Name: discord id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.discord ALTER COLUMN id SET DEFAULT nextval('league_manager.discord_id_seq'::regclass);


--
-- TOC entry 3074 (class 2604 OID 20886)
-- Name: division id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.division ALTER COLUMN id SET DEFAULT nextval('league_manager.division_id_seq'::regclass);


--
-- TOC entry 3069 (class 2604 OID 20803)
-- Name: event id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.event ALTER COLUMN id SET DEFAULT nextval('league_manager.event_id_seq'::regclass);


--
-- TOC entry 3077 (class 2604 OID 20936)
-- Name: final id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.final ALTER COLUMN id SET DEFAULT nextval('league_manager.final_id_seq'::regclass);


--
-- TOC entry 3081 (class 2604 OID 21020)
-- Name: final_results id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.final_results ALTER COLUMN id SET DEFAULT nextval('league_manager.final_results_id_seq'::regclass);


--
-- TOC entry 3082 (class 2604 OID 21043)
-- Name: free_agent id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.free_agent ALTER COLUMN id SET DEFAULT nextval('league_manager.free_agent_id_seq'::regclass);


--
-- TOC entry 3070 (class 2604 OID 20818)
-- Name: league id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.league ALTER COLUMN id SET DEFAULT nextval('league_manager.league_id_seq'::regclass);


--
-- TOC entry 3088 (class 2604 OID 21186)
-- Name: lobby id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.lobby ALTER COLUMN id SET DEFAULT nextval('league_manager.lobby_id_seq'::regclass);


--
-- TOC entry 3083 (class 2604 OID 21061)
-- Name: match id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match ALTER COLUMN id SET DEFAULT nextval('league_manager.match_id_seq'::regclass);


--
-- TOC entry 3089 (class 2604 OID 21199)
-- Name: match_availability id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_availability ALTER COLUMN id SET DEFAULT nextval('league_manager.match_availability_id_seq'::regclass);


--
-- TOC entry 3092 (class 2604 OID 21271)
-- Name: match_data id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_data ALTER COLUMN id SET DEFAULT nextval('league_manager.match_data_id_seq'::regclass);


--
-- TOC entry 3090 (class 2604 OID 21237)
-- Name: match_review id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_review ALTER COLUMN id SET DEFAULT nextval('league_manager.match_review_id_seq'::regclass);


--
-- TOC entry 3091 (class 2604 OID 21258)
-- Name: match_schedule id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_schedule ALTER COLUMN id SET DEFAULT nextval('league_manager.match_schedule_id_seq'::regclass);


--
-- TOC entry 3071 (class 2604 OID 20834)
-- Name: matchtype id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.matchtype ALTER COLUMN id SET DEFAULT nextval('league_manager.matchtype_id_seq'::regclass);


--
-- TOC entry 3065 (class 2604 OID 20752)
-- Name: permission id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.permission ALTER COLUMN id SET DEFAULT nextval('league_manager.permission_id_seq'::regclass);


--
-- TOC entry 3078 (class 2604 OID 20959)
-- Name: player id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player ALTER COLUMN id SET DEFAULT nextval('league_manager.player_id_seq'::regclass);


--
-- TOC entry 3084 (class 2604 OID 21094)
-- Name: player_award id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_award ALTER COLUMN id SET DEFAULT nextval('league_manager.player_award_id_seq'::regclass);


--
-- TOC entry 3093 (class 2604 OID 21284)
-- Name: player_match_data id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_match_data ALTER COLUMN id SET DEFAULT nextval('league_manager.player_match_data_id_seq'::regclass);


--
-- TOC entry 3085 (class 2604 OID 21117)
-- Name: player_team id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_team ALTER COLUMN id SET DEFAULT nextval('league_manager.player_team_id_seq'::regclass);


--
-- TOC entry 3075 (class 2604 OID 20899)
-- Name: season id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season ALTER COLUMN id SET DEFAULT nextval('league_manager.season_id_seq'::regclass);


--
-- TOC entry 3076 (class 2604 OID 20918)
-- Name: season_division id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_division ALTER COLUMN id SET DEFAULT nextval('league_manager.season_division_id_seq'::regclass);


--
-- TOC entry 3079 (class 2604 OID 20979)
-- Name: season_division_team id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_division_team ALTER COLUMN id SET DEFAULT nextval('league_manager.season_division_team_id_seq'::regclass);


--
-- TOC entry 3086 (class 2604 OID 21135)
-- Name: season_registration id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_registration ALTER COLUMN id SET DEFAULT nextval('league_manager.season_registration_id_seq'::regclass);


--
-- TOC entry 3066 (class 2604 OID 20768)
-- Name: team id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team ALTER COLUMN id SET DEFAULT nextval('league_manager.team_id_seq'::regclass);


--
-- TOC entry 3080 (class 2604 OID 20997)
-- Name: team_award id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team_award ALTER COLUMN id SET DEFAULT nextval('league_manager.team_award_id_seq'::regclass);


--
-- TOC entry 3087 (class 2604 OID 21163)
-- Name: team_invites id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team_invites ALTER COLUMN id SET DEFAULT nextval('league_manager.team_invites_id_seq'::regclass);


--
-- TOC entry 3072 (class 2604 OID 20854)
-- Name: twitch id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.twitch ALTER COLUMN id SET DEFAULT nextval('league_manager.twitch_id_seq'::regclass);


--
-- TOC entry 3067 (class 2604 OID 20778)
-- Name: user id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager."user" ALTER COLUMN id SET DEFAULT nextval('league_manager.user_id_seq'::regclass);


--
-- TOC entry 3073 (class 2604 OID 20868)
-- Name: user_permissions id; Type: DEFAULT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.user_permissions ALTER COLUMN id SET DEFAULT nextval('league_manager.user_permissions_id_seq'::regclass);


--
-- TOC entry 3379 (class 0 OID 20717)
-- Dependencies: 207
-- Data for Name: arena; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.arena VALUES ('Colosseum', 'Colosseum', NULL);
INSERT INTO league_manager.arena VALUES ('Island', 'Island', NULL);
INSERT INTO league_manager.arena VALUES ('Obstacles', 'Obstacles', NULL);
INSERT INTO league_manager.arena VALUES ('Obstacles_XL', 'Obstacles XL', NULL);
INSERT INTO league_manager.arena VALUES ('Slapstadium', 'Slapstadium', 'Standard ice hockey stadium');
INSERT INTO league_manager.arena VALUES ('Slapstadium_Mini', 'Slapstadium Mini', 'Mini ice hockey stadium');
INSERT INTO league_manager.arena VALUES ('Slapstadium_XL', 'Slapstadium XL', 'Extra Large ice hockey stadium');
INSERT INTO league_manager.arena VALUES ('Slapstation', 'Slapstation', NULL);
INSERT INTO league_manager.arena VALUES ('Slapville', 'Slapville', NULL);
INSERT INTO league_manager.arena VALUES ('Slapville_Jumbo', 'Slapville Jumbo', NULL);
INSERT INTO league_manager.arena VALUES ('Table_Hockey ', 'Table Hockey ', NULL);


--
-- TOC entry 3381 (class 0 OID 20726)
-- Dependencies: 209
-- Data for Name: award; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3392 (class 0 OID 20786)
-- Dependencies: 220
-- Data for Name: discord; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.discord VALUES (9, '202990104170463241', 2, '3m6uVxZwe0ms0CCm7mXisP3f6ywqNL', 'CzpGOtquncnvYMocY4NmF5icLPrZO1', NULL);


--
-- TOC entry 3404 (class 0 OID 20883)
-- Dependencies: 232
-- Data for Name: division; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.division VALUES (1, 'Pro League', 1, 'PL', 'jfatass dreams of winning');
INSERT INTO league_manager.division VALUES (2, 'Intermediate League', 1, 'IM', 'why is dwarf still here');
INSERT INTO league_manager.division VALUES (3, 'Open League', 1, 'OL', '2C1F the real goats');
INSERT INTO league_manager.division VALUES (4, 'Single League', 1, 'SL', 'Where it all started');
INSERT INTO league_manager.division VALUES (5, 'Spar Division', 1, 'Spar', 'Draft league division');
INSERT INTO league_manager.division VALUES (6, 'Ness Division', 1, 'Ness', 'Draft league division');


--
-- TOC entry 3382 (class 0 OID 20733)
-- Dependencies: 210
-- Data for Name: end_reason; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.end_reason VALUES ('AwayTeamLeft', 'Away Team left', NULL);
INSERT INTO league_manager.end_reason VALUES ('Cancelled', 'Cancelled', NULL);
INSERT INTO league_manager.end_reason VALUES ('EndOfRegulation', 'End of Regulation', NULL);
INSERT INTO league_manager.end_reason VALUES ('Forfeit', 'Forfeit', NULL);
INSERT INTO league_manager.end_reason VALUES ('HomeTeamLeft', 'Home Team left', NULL);
INSERT INTO league_manager.end_reason VALUES ('MercyRule', 'Mercy', NULL);
INSERT INTO league_manager.end_reason VALUES ('Overtime', 'Overtime', NULL);
INSERT INTO league_manager.end_reason VALUES ('Tie', 'Tie', NULL);
INSERT INTO league_manager.end_reason VALUES ('Unknown', 'Unknown', NULL);


--
-- TOC entry 3394 (class 0 OID 20800)
-- Dependencies: 222
-- Data for Name: event; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3410 (class 0 OID 20933)
-- Dependencies: 238
-- Data for Name: final; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3418 (class 0 OID 21017)
-- Dependencies: 246
-- Data for Name: final_results; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3420 (class 0 OID 21040)
-- Dependencies: 248
-- Data for Name: free_agent; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.free_agent VALUES (1, 40, 2, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (2, 8, 2, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (3, 20, 2, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (4, 41, 2, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (5, 42, 2, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (6, 43, 2, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (7, 44, 2, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (8, 45, 2, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (9, 96, 4, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (10, 97, 4, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (11, 39, 4, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (12, 44, 4, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (13, 98, 4, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (14, 19, 6, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (15, 19, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (16, 80, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (17, 148, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (18, 90, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (19, 149, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (20, 150, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (21, 151, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (22, 100, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (23, 71, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (24, 152, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (25, 153, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (26, 55, 8, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (27, 161, 11, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (28, 151, 11, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (29, 96, 11, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (30, 150, 11, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (31, 19, 5, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (32, 123, 5, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (33, 120, 5, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (34, 89, 7, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (35, 55, 7, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (36, 132, 7, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (37, 151, 7, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (38, 80, 7, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (39, 90, 7, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (40, 83, 9, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (41, 80, 10, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (42, 107, 10, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (43, 96, 10, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (44, 167, 10, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (45, 112, 10, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (46, 155, 14, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (47, 24, 14, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (48, 165, 15, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (49, 78, 15, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (50, 143, 16, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (51, 173, 16, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (52, 175, 17, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (53, 48, 17, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (54, 18, 17, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (55, 19, 17, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (56, 176, 17, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (57, 151, 19, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (58, 48, 19, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (59, 90, 19, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (60, 188, 19, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (61, 225, 20, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (62, 155, 20, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (63, 226, 20, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (64, 227, 20, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (65, 228, 20, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (66, 201, 21, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (67, 17, 21, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (68, 201, 22, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (69, 79, 23, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (70, 157, 23, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (71, 156, 23, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (72, 48, 24, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (73, 158, 26, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (74, 221, 27, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (75, 201, 27, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (76, 249, 27, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (77, 90, 27, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (78, 171, 27, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (79, 90, 28, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (80, 18, 28, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (81, 276, 28, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (82, 165, 29, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (83, 90, 29, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (84, 247, 30, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (85, 48, 30, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (86, 158, 30, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (87, 79, 30, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (88, 250, 30, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (89, 90, 30, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (90, 228, 30, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (91, 154, 31, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (92, 1, 31, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (93, 292, 31, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (94, 54, 31, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (95, 276, 32, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (96, 293, 32, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (97, 299, 33, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (98, 296, 33, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (99, 297, 33, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (100, 298, 33, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (101, 301, 33, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (102, 257, 35, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (103, 207, 35, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (104, 156, 35, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (105, 308, 36, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (106, 219, 36, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (107, 270, 36, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (108, 205, 37, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (109, 207, 38, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (110, 90, 38, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (111, 257, 38, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (112, 186, 38, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (113, 171, 38, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (114, 161, 38, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (115, 361, 39, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (116, 316, 39, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (117, 362, 39, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (118, 363, 39, NULL, NULL);
INSERT INTO league_manager.free_agent VALUES (119, 303, 39, NULL, NULL);


--
-- TOC entry 3383 (class 0 OID 20740)
-- Dependencies: 211
-- Data for Name: game_mode; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.game_mode VALUES ('dodgepuck', 'Dodgepuck', 'Don''t get hit!');
INSERT INTO league_manager.game_mode VALUES ('hockey', 'Hockey', 'The default gamemode');
INSERT INTO league_manager.game_mode VALUES ('tag', 'Tag', 'Chase or be chased!');


--
-- TOC entry 3396 (class 0 OID 20815)
-- Dependencies: 224
-- Data for Name: league; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.league VALUES (1, 'Oceanic Slapshot League', 'OSL', 'oce-east');


--
-- TOC entry 3432 (class 0 OID 21183)
-- Dependencies: 260
-- Data for Name: lobby; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3422 (class 0 OID 21058)
-- Dependencies: 250
-- Data for Name: match; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3434 (class 0 OID 21196)
-- Dependencies: 262
-- Data for Name: match_availability; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3441 (class 0 OID 21268)
-- Dependencies: 269
-- Data for Name: match_data; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3435 (class 0 OID 21212)
-- Dependencies: 263
-- Data for Name: match_result; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3437 (class 0 OID 21234)
-- Dependencies: 265
-- Data for Name: match_review; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3439 (class 0 OID 21255)
-- Dependencies: 267
-- Data for Name: match_schedule; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3398 (class 0 OID 20831)
-- Dependencies: 226
-- Data for Name: matchtype; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.matchtype VALUES (1, 'Competitive', 'Standard format for league matches', true, 'Slapstadium', 0, 300, 'hockey', 6);
INSERT INTO league_manager.matchtype VALUES (2, 'Casual', 'Short 5 minute game', false, 'Slapstadium', 0, 300, 'hockey', 6);
INSERT INTO league_manager.matchtype VALUES (3, 'Twos', '2v2 Competitive', true, 'Slapstadium_Mini', 0, 300, 'hockey', 4);


--
-- TOC entry 3385 (class 0 OID 20749)
-- Dependencies: 213
-- Data for Name: permission; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.permission VALUES (1, 'admin', 'Site Administrator');
INSERT INTO league_manager.permission VALUES (2, 'leag_comm', 'League Commissioner');
INSERT INTO league_manager.permission VALUES (3, 'leag_coord', 'League Coordinator');
INSERT INTO league_manager.permission VALUES (4, 'team_manager', 'Team Manager');
INSERT INTO league_manager.permission VALUES (5, 'team_owner', 'Team Owner');
INSERT INTO league_manager.permission VALUES (6, 'streamer', 'Twitch Streamer');


--
-- TOC entry 3412 (class 0 OID 20956)
-- Dependencies: 240
-- Data for Name: player; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.player VALUES (1, 155, NULL, 'Eagle', false, 1, NULL);
INSERT INTO league_manager.player VALUES (2, NULL, NULL, '!Son', false, 1, NULL);
INSERT INTO league_manager.player VALUES (3, 641, NULL, 'Jakew100', false, 1, NULL);
INSERT INTO league_manager.player VALUES (4, NULL, NULL, 'Palap', false, 1, NULL);
INSERT INTO league_manager.player VALUES (5, NULL, NULL, 'Dekruz', false, 1, NULL);
INSERT INTO league_manager.player VALUES (6, NULL, NULL, 'Arctic Hunter', false, 1, NULL);
INSERT INTO league_manager.player VALUES (7, NULL, NULL, 'Freeky_Meeky', false, 1, NULL);
INSERT INTO league_manager.player VALUES (8, NULL, NULL, 'Nicko', false, 1, NULL);
INSERT INTO league_manager.player VALUES (9, NULL, NULL, 'Lando', false, 1, NULL);
INSERT INTO league_manager.player VALUES (10, NULL, NULL, 'Goddard', false, 1, NULL);
INSERT INTO league_manager.player VALUES (11, NULL, NULL, 'CastleOCE', false, 1, NULL);
INSERT INTO league_manager.player VALUES (12, 633, NULL, 'Ness', false, 1, NULL);
INSERT INTO league_manager.player VALUES (13, 96337, NULL, 'Pewdekz', false, 1, NULL);
INSERT INTO league_manager.player VALUES (14, NULL, NULL, 'Juronn', false, 1, NULL);
INSERT INTO league_manager.player VALUES (15, NULL, NULL, 'Big Money', false, 1, NULL);
INSERT INTO league_manager.player VALUES (16, NULL, NULL, 'Jake', false, 1, NULL);
INSERT INTO league_manager.player VALUES (17, 162, NULL, 'egyptian messi', false, 1, NULL);
INSERT INTO league_manager.player VALUES (18, 662, NULL, 'Rogann', false, 1, NULL);
INSERT INTO league_manager.player VALUES (19, 571, NULL, 'SkdragoN', false, 1, NULL);
INSERT INTO league_manager.player VALUES (20, NULL, NULL, 'Tiipps', false, 1, NULL);
INSERT INTO league_manager.player VALUES (21, 664, NULL, 'Mukey', false, 1, NULL);
INSERT INTO league_manager.player VALUES (22, NULL, NULL, 'Kungfutyla', false, 2, NULL);
INSERT INTO league_manager.player VALUES (23, NULL, NULL, 'Lapine', false, 2, NULL);
INSERT INTO league_manager.player VALUES (24, 663, NULL, 'EliteAlex', false, 2, NULL);
INSERT INTO league_manager.player VALUES (25, NULL, NULL, 'Tom Cruise', false, 2, NULL);
INSERT INTO league_manager.player VALUES (26, NULL, NULL, 'Luniic', false, 2, NULL);
INSERT INTO league_manager.player VALUES (27, NULL, NULL, 'JarJarTwinks', false, 2, NULL);
INSERT INTO league_manager.player VALUES (28, 161, NULL, 'Kyle', false, 2, NULL);
INSERT INTO league_manager.player VALUES (29, NULL, NULL, 'Wolomon', false, 2, NULL);
INSERT INTO league_manager.player VALUES (30, NULL, NULL, 'Yeke Yeke', false, 2, NULL);
INSERT INTO league_manager.player VALUES (31, NULL, NULL, 'JJ', false, 2, NULL);
INSERT INTO league_manager.player VALUES (32, NULL, NULL, 'D_K', false, 2, NULL);
INSERT INTO league_manager.player VALUES (33, NULL, NULL, 'Plus', false, 2, NULL);
INSERT INTO league_manager.player VALUES (34, NULL, NULL, 'Jordz', false, 2, NULL);
INSERT INTO league_manager.player VALUES (35, NULL, NULL, 'Brodog', false, 2, NULL);
INSERT INTO league_manager.player VALUES (36, NULL, NULL, 'Aarron89', false, 2, NULL);
INSERT INTO league_manager.player VALUES (37, NULL, NULL, 'Xplax', false, 2, NULL);
INSERT INTO league_manager.player VALUES (38, 81, NULL, 'Krypto', false, 2, NULL);
INSERT INTO league_manager.player VALUES (39, NULL, NULL, 'Sapster', false, 2, NULL);
INSERT INTO league_manager.player VALUES (40, NULL, NULL, 'Nutterz', false, 2, NULL);
INSERT INTO league_manager.player VALUES (41, NULL, NULL, 'Jekker', false, 2, NULL);
INSERT INTO league_manager.player VALUES (42, NULL, NULL, 'Sconeboy', false, 2, NULL);
INSERT INTO league_manager.player VALUES (43, NULL, NULL, 'Storm', false, 2, NULL);
INSERT INTO league_manager.player VALUES (44, NULL, NULL, 'Compano', false, 2, NULL);
INSERT INTO league_manager.player VALUES (45, NULL, NULL, 'Bruby', false, 2, NULL);
INSERT INTO league_manager.player VALUES (46, NULL, NULL, 'USGOVERNMENT', false, 3, NULL);
INSERT INTO league_manager.player VALUES (47, NULL, NULL, 'YekeYeke', false, 3, NULL);
INSERT INTO league_manager.player VALUES (48, 179, NULL, 'Nananana', false, 3, NULL);
INSERT INTO league_manager.player VALUES (49, NULL, NULL, 'Hawk', false, 3, NULL);
INSERT INTO league_manager.player VALUES (50, NULL, NULL, 'Wafflerus', false, 4, NULL);
INSERT INTO league_manager.player VALUES (51, 504, NULL, 'BigD', false, 4, NULL);
INSERT INTO league_manager.player VALUES (52, NULL, NULL, 'The Spin', false, 4, NULL);
INSERT INTO league_manager.player VALUES (53, NULL, NULL, 'Turtle Frog', false, 4, NULL);
INSERT INTO league_manager.player VALUES (54, 157, NULL, 'n1q', false, 4, NULL);
INSERT INTO league_manager.player VALUES (55, 917, NULL, 'Q.E.D', false, 4, NULL);
INSERT INTO league_manager.player VALUES (56, NULL, NULL, 'HaydosRun', false, 4, NULL);
INSERT INTO league_manager.player VALUES (57, NULL, NULL, 'IFC Soviet', false, 4, NULL);
INSERT INTO league_manager.player VALUES (58, NULL, NULL, 'Doofey', false, 4, NULL);
INSERT INTO league_manager.player VALUES (59, NULL, NULL, 'legit (guh)', false, 4, NULL);
INSERT INTO league_manager.player VALUES (60, NULL, NULL, 'Giant Stepps', false, 4, NULL);
INSERT INTO league_manager.player VALUES (61, NULL, NULL, 'Jorr', false, 4, NULL);
INSERT INTO league_manager.player VALUES (62, NULL, NULL, 'smwoss', false, 4, NULL);
INSERT INTO league_manager.player VALUES (63, NULL, NULL, 'ShadowStorm', false, 4, NULL);
INSERT INTO league_manager.player VALUES (64, NULL, NULL, 'CONMAN', false, 4, NULL);
INSERT INTO league_manager.player VALUES (65, NULL, NULL, 'BilboLaggins', false, 4, NULL);
INSERT INTO league_manager.player VALUES (66, NULL, NULL, 'Qlo', false, 4, NULL);
INSERT INTO league_manager.player VALUES (67, NULL, NULL, 'Bruhment', false, 4, NULL);
INSERT INTO league_manager.player VALUES (68, NULL, NULL, 'RedCadeaux', false, 4, NULL);
INSERT INTO league_manager.player VALUES (69, NULL, NULL, 'nubless nuble', false, 4, NULL);
INSERT INTO league_manager.player VALUES (70, NULL, NULL, 'CptCodes', false, 4, NULL);
INSERT INTO league_manager.player VALUES (71, NULL, NULL, 'Stelios', false, 4, NULL);
INSERT INTO league_manager.player VALUES (72, NULL, NULL, 'Antotron', false, 4, NULL);
INSERT INTO league_manager.player VALUES (73, NULL, NULL, 'positive only', false, 4, NULL);
INSERT INTO league_manager.player VALUES (74, 84, NULL, 'Godric', false, 4, NULL);
INSERT INTO league_manager.player VALUES (75, NULL, NULL, 'aczii', false, 4, NULL);
INSERT INTO league_manager.player VALUES (76, 214, NULL, 'Steezy', false, 4, NULL);
INSERT INTO league_manager.player VALUES (77, NULL, NULL, 'GiraffeAmongMen', false, 4, NULL);
INSERT INTO league_manager.player VALUES (78, 1778, NULL, 'Sadville', false, 4, NULL);
INSERT INTO league_manager.player VALUES (79, 151, NULL, 'aros', false, 4, NULL);
INSERT INTO league_manager.player VALUES (80, 174, NULL, 'Cheeki Breeki', false, 4, NULL);
INSERT INTO league_manager.player VALUES (81, NULL, NULL, 'DByss', false, 4, NULL);
INSERT INTO league_manager.player VALUES (82, 517, NULL, 'The Labrador', false, 4, NULL);
INSERT INTO league_manager.player VALUES (83, NULL, NULL, 'Fuzza', false, 4, NULL);
INSERT INTO league_manager.player VALUES (84, 147, NULL, 'CooperG03', false, 4, NULL);
INSERT INTO league_manager.player VALUES (85, 152, NULL, 'Zanich', false, 4, NULL);
INSERT INTO league_manager.player VALUES (86, NULL, NULL, 'BobTooBad', false, 4, NULL);
INSERT INTO league_manager.player VALUES (87, NULL, NULL, 'Aza', false, 4, NULL);
INSERT INTO league_manager.player VALUES (88, 158, NULL, 'Spooky', false, 4, NULL);
INSERT INTO league_manager.player VALUES (89, NULL, NULL, 'Doomicus', false, 4, NULL);
INSERT INTO league_manager.player VALUES (90, 128, NULL, 'GurGur', false, 4, NULL);
INSERT INTO league_manager.player VALUES (91, NULL, NULL, 'TendyWendy', false, 4, NULL);
INSERT INTO league_manager.player VALUES (92, NULL, NULL, 'jaina', false, 4, NULL);
INSERT INTO league_manager.player VALUES (93, NULL, NULL, 'Good Guy Greg', false, 4, NULL);
INSERT INTO league_manager.player VALUES (94, NULL, NULL, 'Jon', false, 4, NULL);
INSERT INTO league_manager.player VALUES (95, NULL, NULL, 'beter', false, 4, NULL);
INSERT INTO league_manager.player VALUES (96, 10612, NULL, 'Halal', false, 4, NULL);
INSERT INTO league_manager.player VALUES (97, NULL, NULL, 'Bantz', false, 4, NULL);
INSERT INTO league_manager.player VALUES (98, NULL, NULL, 'pastelzi', false, 4, NULL);
INSERT INTO league_manager.player VALUES (99, NULL, NULL, 'mogu.', false, 6, NULL);
INSERT INTO league_manager.player VALUES (100, NULL, NULL, 'wae.', false, 6, NULL);
INSERT INTO league_manager.player VALUES (101, NULL, NULL, 'LilacPlays', false, 6, NULL);
INSERT INTO league_manager.player VALUES (102, NULL, NULL, 'White Haired Princess', false, 6, NULL);
INSERT INTO league_manager.player VALUES (103, NULL, NULL, 'riotgrill', false, 6, NULL);
INSERT INTO league_manager.player VALUES (104, NULL, NULL, 'Brosenich', false, 6, NULL);
INSERT INTO league_manager.player VALUES (105, NULL, NULL, 'nothinc', false, 6, NULL);
INSERT INTO league_manager.player VALUES (106, NULL, NULL, 'Maracter', false, 6, NULL);
INSERT INTO league_manager.player VALUES (107, NULL, NULL, 'Yallambie Maccas', false, 6, NULL);
INSERT INTO league_manager.player VALUES (108, NULL, NULL, 'AB05', false, 6, NULL);
INSERT INTO league_manager.player VALUES (109, NULL, NULL, 'martin', false, 6, NULL);
INSERT INTO league_manager.player VALUES (110, NULL, NULL, 'Wizardeath', false, 6, NULL);
INSERT INTO league_manager.player VALUES (111, NULL, NULL, 'car going pass maccas', false, 6, NULL);
INSERT INTO league_manager.player VALUES (112, NULL, NULL, 'Platypus', false, 6, NULL);
INSERT INTO league_manager.player VALUES (113, 66, NULL, 'Spar', false, 6, NULL);
INSERT INTO league_manager.player VALUES (114, NULL, NULL, 'SuchIsLife', false, 6, NULL);
INSERT INTO league_manager.player VALUES (115, NULL, NULL, 'Youngy', false, 6, NULL);
INSERT INTO league_manager.player VALUES (116, 578, NULL, 'aha yeah baby', false, 6, NULL);
INSERT INTO league_manager.player VALUES (117, NULL, NULL, 'Pabrico Willis', false, 6, NULL);
INSERT INTO league_manager.player VALUES (118, NULL, NULL, 'BOT Matt', false, 6, NULL);
INSERT INTO league_manager.player VALUES (119, 154, NULL, 'baccy', false, 5, NULL);
INSERT INTO league_manager.player VALUES (120, NULL, NULL, 'moohay', false, 5, NULL);
INSERT INTO league_manager.player VALUES (121, 204906, NULL, 'Zoe', false, 8, NULL);
INSERT INTO league_manager.player VALUES (122, NULL, NULL, 'Hef', false, 8, NULL);
INSERT INTO league_manager.player VALUES (123, NULL, NULL, 'Bruhpo', false, 8, NULL);
INSERT INTO league_manager.player VALUES (124, NULL, NULL, 'BOT Kris', false, 8, NULL);
INSERT INTO league_manager.player VALUES (125, 649, NULL, 'Mightymichael', false, 8, NULL);
INSERT INTO league_manager.player VALUES (126, NULL, NULL, 'yum', false, 8, NULL);
INSERT INTO league_manager.player VALUES (127, 516, NULL, 'chabana', false, 8, NULL);
INSERT INTO league_manager.player VALUES (128, 525, NULL, 'Zemix', false, 8, NULL);
INSERT INTO league_manager.player VALUES (129, NULL, NULL, 'Rias Grimory', false, 8, NULL);
INSERT INTO league_manager.player VALUES (130, 576, NULL, 'Levy', false, 8, NULL);
INSERT INTO league_manager.player VALUES (131, NULL, NULL, 'BlondeBeach', false, 8, NULL);
INSERT INTO league_manager.player VALUES (132, NULL, NULL, 'jimmy da best', false, 8, NULL);
INSERT INTO league_manager.player VALUES (133, NULL, NULL, 'Dandy', false, 8, NULL);
INSERT INTO league_manager.player VALUES (134, NULL, NULL, 'alfie', false, 8, NULL);
INSERT INTO league_manager.player VALUES (135, 648, NULL, 'Turgulu', false, 8, NULL);
INSERT INTO league_manager.player VALUES (136, NULL, NULL, 'Macka', false, 8, NULL);
INSERT INTO league_manager.player VALUES (137, 325, NULL, 'endEd', false, 8, NULL);
INSERT INTO league_manager.player VALUES (138, NULL, NULL, 'Sexy Turtle', false, 8, NULL);
INSERT INTO league_manager.player VALUES (139, NULL, NULL, 'Capy', false, 8, NULL);
INSERT INTO league_manager.player VALUES (140, 725, NULL, 'youngboris', false, 8, NULL);
INSERT INTO league_manager.player VALUES (141, 1550, NULL, 'PepegaPig', false, 8, NULL);
INSERT INTO league_manager.player VALUES (142, NULL, NULL, 'NotAWeeb', false, 8, NULL);
INSERT INTO league_manager.player VALUES (143, 1750, NULL, 'Beef Stew', false, 8, NULL);
INSERT INTO league_manager.player VALUES (144, 39079, NULL, 'iMinnq', false, 8, NULL);
INSERT INTO league_manager.player VALUES (145, NULL, NULL, '12GAIGE', false, 8, NULL);
INSERT INTO league_manager.player VALUES (146, 600, NULL, 'h0ppy', false, 8, NULL);
INSERT INTO league_manager.player VALUES (147, 574, NULL, 'skitz', false, 8, NULL);
INSERT INTO league_manager.player VALUES (148, NULL, NULL, 'GrumpyBiscuit', false, 8, NULL);
INSERT INTO league_manager.player VALUES (149, NULL, NULL, 'AngusB37', false, 8, NULL);
INSERT INTO league_manager.player VALUES (150, 659, NULL, 'homme', false, 8, NULL);
INSERT INTO league_manager.player VALUES (151, 2051, NULL, 'poop', false, 8, NULL);
INSERT INTO league_manager.player VALUES (152, NULL, NULL, 'kaoski', false, 8, NULL);
INSERT INTO league_manager.player VALUES (153, 246059, NULL, 'StaticTurtle', false, 8, NULL);
INSERT INTO league_manager.player VALUES (154, 598, NULL, 'Chebs', false, 14, NULL);
INSERT INTO league_manager.player VALUES (155, 116462, NULL, 'Socolski', false, 14, NULL);
INSERT INTO league_manager.player VALUES (156, 91688, NULL, 'Sinko', false, 15, NULL);
INSERT INTO league_manager.player VALUES (157, 91687, NULL, 'MassiveLegend', false, 15, NULL);
INSERT INTO league_manager.player VALUES (158, 147030, NULL, 'egyptian forehead', false, 15, NULL);
INSERT INTO league_manager.player VALUES (159, 1427, NULL, 'Arrow', false, 15, NULL);
INSERT INTO league_manager.player VALUES (160, 1379, NULL, 'kubix', false, 11, NULL);
INSERT INTO league_manager.player VALUES (161, 669, NULL, 'miniskirt', false, 15, NULL);
INSERT INTO league_manager.player VALUES (162, 78204, NULL, 'Joycey', false, 15, NULL);
INSERT INTO league_manager.player VALUES (163, 101903, NULL, 'GEX', false, 15, NULL);
INSERT INTO league_manager.player VALUES (164, 78431, NULL, 'Juice15', false, 15, NULL);
INSERT INTO league_manager.player VALUES (165, 235517, NULL, 'FLACKO', false, 15, NULL);
INSERT INTO league_manager.player VALUES (166, 197770, NULL, 'Nugget', false, 16, NULL);
INSERT INTO league_manager.player VALUES (167, 7237, NULL, 'ant', false, 16, NULL);
INSERT INTO league_manager.player VALUES (168, 152189, NULL, 'Cdowny99', false, 16, NULL);
INSERT INTO league_manager.player VALUES (169, 155519, NULL, 'Jims Onlyfans', false, 16, NULL);
INSERT INTO league_manager.player VALUES (170, 124045, NULL, 'abluh', false, 16, NULL);
INSERT INTO league_manager.player VALUES (171, 124042, NULL, 'SnowWolf', false, 16, NULL);
INSERT INTO league_manager.player VALUES (172, 124044, NULL, 'CowArmy33', false, 16, NULL);
INSERT INTO league_manager.player VALUES (173, 11208, NULL, 'citrus clown', false, 16, NULL);
INSERT INTO league_manager.player VALUES (174, 91818, NULL, 'Da Don', false, 16, NULL);
INSERT INTO league_manager.player VALUES (175, 260452, NULL, 'Blister', false, 16, NULL);
INSERT INTO league_manager.player VALUES (176, 124017, NULL, 'naomi', false, 18, NULL);
INSERT INTO league_manager.player VALUES (177, 286864, NULL, 'poisy', false, 18, NULL);
INSERT INTO league_manager.player VALUES (178, 301296, NULL, 'deccy p', false, 18, NULL);
INSERT INTO league_manager.player VALUES (179, 301294, NULL, 'HaydosTG04', false, 18, NULL);
INSERT INTO league_manager.player VALUES (180, 301295, NULL, 'illyway', false, 18, NULL);
INSERT INTO league_manager.player VALUES (181, 301289, NULL, 'KTF', false, 18, NULL);
INSERT INTO league_manager.player VALUES (182, 332258, NULL, 'Adorius', false, 18, NULL);
INSERT INTO league_manager.player VALUES (183, 353631, NULL, 'Dr Zoidberg', false, 18, NULL);
INSERT INTO league_manager.player VALUES (184, 334966, NULL, 'grandmaster ramen', false, 18, NULL);
INSERT INTO league_manager.player VALUES (185, 332180, NULL, 'John Herolds', false, 18, NULL);
INSERT INTO league_manager.player VALUES (186, 329359, NULL, 'Rabbit', false, 18, NULL);
INSERT INTO league_manager.player VALUES (187, 294036, NULL, 'Chad', false, 18, NULL);
INSERT INTO league_manager.player VALUES (188, 182, NULL, 'duc nhan', false, 18, NULL);
INSERT INTO league_manager.player VALUES (189, 337857, NULL, 'Mxdic', false, 18, NULL);
INSERT INTO league_manager.player VALUES (190, 318219, NULL, 'Bumblebee24', false, 18, NULL);
INSERT INTO league_manager.player VALUES (191, 345043, NULL, 'Jonahmic14', false, 18, NULL);
INSERT INTO league_manager.player VALUES (192, 277948, NULL, 'zac', false, 18, NULL);
INSERT INTO league_manager.player VALUES (193, 435463, NULL, 'amie', false, 20, NULL);
INSERT INTO league_manager.player VALUES (194, 441171, NULL, 'antonio_', false, 20, NULL);
INSERT INTO league_manager.player VALUES (195, 443475, NULL, 'jambon', false, 20, NULL);
INSERT INTO league_manager.player VALUES (196, 443476, NULL, 'ANCIENT', false, 20, NULL);
INSERT INTO league_manager.player VALUES (197, 443483, NULL, 'hqckk', false, 20, NULL);
INSERT INTO league_manager.player VALUES (198, 444420, NULL, 'heroinfather', false, 20, NULL);
INSERT INTO league_manager.player VALUES (199, 195233, NULL, 'BabaJ', false, 20, NULL);
INSERT INTO league_manager.player VALUES (200, 195243, NULL, 'AZTEK', false, 20, NULL);
INSERT INTO league_manager.player VALUES (201, 401504, NULL, 'Hyquin', false, 20, NULL);
INSERT INTO league_manager.player VALUES (202, 374530, NULL, 'chim.os', false, 20, NULL);
INSERT INTO league_manager.player VALUES (203, 374555, NULL, 'josh4813', false, 20, NULL);
INSERT INTO league_manager.player VALUES (204, 376979, NULL, 'billbakker', false, 20, NULL);
INSERT INTO league_manager.player VALUES (205, 379756, NULL, 'boppy', false, 20, NULL);
INSERT INTO league_manager.player VALUES (206, 302381, NULL, 'samslayz246', false, 20, NULL);
INSERT INTO league_manager.player VALUES (207, 149686, NULL, 'Forge', false, 20, NULL);
INSERT INTO league_manager.player VALUES (208, 428831, NULL, 'Ham', false, 20, NULL);
INSERT INTO league_manager.player VALUES (209, 429551, NULL, 'mfunc1', false, 20, NULL);
INSERT INTO league_manager.player VALUES (210, 279865, NULL, 'Leddy', false, 20, NULL);
INSERT INTO league_manager.player VALUES (211, 392038, NULL, 'NaCl', false, 20, NULL);
INSERT INTO league_manager.player VALUES (212, 428829, NULL, 'Belacqua', false, 20, NULL);
INSERT INTO league_manager.player VALUES (213, 429744, NULL, 'Demo', false, 20, NULL);
INSERT INTO league_manager.player VALUES (214, 413214, NULL, 'Happy Rat', false, 20, NULL);
INSERT INTO league_manager.player VALUES (215, 413215, NULL, 'LittleHead', false, 20, NULL);
INSERT INTO league_manager.player VALUES (216, 423500, NULL, 'Nutty Professor', false, 20, NULL);
INSERT INTO league_manager.player VALUES (217, 424848, NULL, 'Stinky', false, 20, NULL);
INSERT INTO league_manager.player VALUES (218, 428777, NULL, 'Ridgey', false, 20, NULL);
INSERT INTO league_manager.player VALUES (219, 428807, NULL, 'itag', false, 20, NULL);
INSERT INTO league_manager.player VALUES (220, 428808, NULL, 'Chief', false, 20, NULL);
INSERT INTO league_manager.player VALUES (221, 430900, NULL, 'Nooga', false, 20, NULL);
INSERT INTO league_manager.player VALUES (222, 428778, NULL, 'elfitzo', false, 20, NULL);
INSERT INTO league_manager.player VALUES (223, 428781, NULL, 'Vexation', false, 20, NULL);
INSERT INTO league_manager.player VALUES (224, 429652, NULL, 'Munby', false, 20, NULL);
INSERT INTO league_manager.player VALUES (225, 444199, NULL, 'Limboghini', false, 20, NULL);
INSERT INTO league_manager.player VALUES (226, 447104, NULL, 'grasssyboi', false, 20, NULL);
INSERT INTO league_manager.player VALUES (227, 33232, NULL, 'toMAHto', false, 20, NULL);
INSERT INTO league_manager.player VALUES (228, 452167, NULL, 'FVEK', false, 20, NULL);
INSERT INTO league_manager.player VALUES (229, 327444, NULL, 'dom', false, 22, NULL);
INSERT INTO league_manager.player VALUES (230, 327445, NULL, 'Trebor', false, 22, NULL);
INSERT INTO league_manager.player VALUES (231, 328369, NULL, 'Nizzle', false, 22, NULL);
INSERT INTO league_manager.player VALUES (232, 328725, NULL, 'Priceys', false, 22, NULL);
INSERT INTO league_manager.player VALUES (233, 327475, NULL, 'AutistAuto', false, 22, NULL);
INSERT INTO league_manager.player VALUES (234, NULL, NULL, 'Podasio', false, 22, NULL);
INSERT INTO league_manager.player VALUES (235, NULL, NULL, 'TokyoGhoulLover123', false, 22, NULL);
INSERT INTO league_manager.player VALUES (236, 325969, NULL, 'V39', false, 22, NULL);
INSERT INTO league_manager.player VALUES (237, 325974, NULL, 'p1', false, 22, NULL);
INSERT INTO league_manager.player VALUES (238, 325891, NULL, 'Jberone', false, 22, NULL);
INSERT INTO league_manager.player VALUES (239, 358129, NULL, 'iamVill', false, 22, NULL);
INSERT INTO league_manager.player VALUES (240, 1498, NULL, 'buffy', false, 22, NULL);
INSERT INTO league_manager.player VALUES (241, 1500, NULL, 'Springboxer', false, 11, NULL);
INSERT INTO league_manager.player VALUES (242, 1501, NULL, 'Kongo Kawk', false, 11, NULL);
INSERT INTO league_manager.player VALUES (243, 1502, NULL, 'Cmlar', false, 22, NULL);
INSERT INTO league_manager.player VALUES (244, 1499, NULL, 'Horace', false, 11, NULL);
INSERT INTO league_manager.player VALUES (245, 357437, NULL, 'Wild_King', false, 22, NULL);
INSERT INTO league_manager.player VALUES (246, 513063, NULL, 'DooT', false, 25, NULL);
INSERT INTO league_manager.player VALUES (247, 592423, NULL, 'tej', false, 25, NULL);
INSERT INTO league_manager.player VALUES (248, 374559, NULL, 'kevali', false, 25, NULL);
INSERT INTO league_manager.player VALUES (249, 376856, NULL, 'j952', false, 25, NULL);
INSERT INTO league_manager.player VALUES (250, 104293, NULL, 'jhili', false, 25, NULL);
INSERT INTO league_manager.player VALUES (251, 104294, NULL, 'maynz', false, 25, NULL);
INSERT INTO league_manager.player VALUES (252, NULL, NULL, 'schocca', false, 25, NULL);
INSERT INTO league_manager.player VALUES (253, 408381, NULL, 'Thomas Yones', false, 25, NULL);
INSERT INTO league_manager.player VALUES (254, 625139, NULL, 'Miqel', false, 25, NULL);
INSERT INTO league_manager.player VALUES (255, 625141, NULL, 'Hope', false, 25, NULL);
INSERT INTO league_manager.player VALUES (256, 69744, NULL, 'AngusB', false, 25, NULL);
INSERT INTO league_manager.player VALUES (257, 611925, NULL, 'Mulibar', false, 25, NULL);
INSERT INTO league_manager.player VALUES (258, 438631, NULL, 'Protein Filled Chicken', false, 25, NULL);
INSERT INTO league_manager.player VALUES (259, 611292, NULL, 'JCR', false, 25, NULL);
INSERT INTO league_manager.player VALUES (260, 330, NULL, 'palfa11', false, 25, NULL);
INSERT INTO league_manager.player VALUES (261, 78446, NULL, 'moses', false, 25, NULL);
INSERT INTO league_manager.player VALUES (262, 94737, NULL, 'TAYLAH IS BAE', false, 25, NULL);
INSERT INTO league_manager.player VALUES (263, 433285, NULL, 'Lucoid', false, 25, NULL);
INSERT INTO league_manager.player VALUES (264, 433988, NULL, 'DitchiestField', false, 25, NULL);
INSERT INTO league_manager.player VALUES (265, 434333, NULL, 'ieattacos', false, 25, NULL);
INSERT INTO league_manager.player VALUES (266, 438982, NULL, 'Leviathan', false, 25, NULL);
INSERT INTO league_manager.player VALUES (267, 434336, NULL, 'vezorek', false, 25, NULL);
INSERT INTO league_manager.player VALUES (268, 9968, NULL, 'nefarious_ape', false, 25, NULL);
INSERT INTO league_manager.player VALUES (269, 83393, NULL, 'Vido', false, 25, NULL);
INSERT INTO league_manager.player VALUES (270, 711172, NULL, 'Mum Is Gone', false, 25, NULL);
INSERT INTO league_manager.player VALUES (271, 62283, NULL, 'valerie', false, 26, NULL);
INSERT INTO league_manager.player VALUES (272, 1560, NULL, 'Omni', false, 27, NULL);
INSERT INTO league_manager.player VALUES (273, 233323, NULL, 'Billy GOAT', false, 27, NULL);
INSERT INTO league_manager.player VALUES (274, 170539, NULL, 'azzaminator', false, 27, NULL);
INSERT INTO league_manager.player VALUES (275, 712821, NULL, 'ricky glen', false, 27, NULL);
INSERT INTO league_manager.player VALUES (276, 744109, NULL, 'SomeOneBeLaggin', false, 27, NULL);
INSERT INTO league_manager.player VALUES (277, 744547, NULL, 'Syth', false, 27, NULL);
INSERT INTO league_manager.player VALUES (278, 745277, NULL, 'Hipjunior', false, 27, NULL);
INSERT INTO league_manager.player VALUES (279, 599, NULL, 'MattyB', false, 27, NULL);
INSERT INTO league_manager.player VALUES (280, 524, NULL, 'WhatTheEh', false, 27, NULL);
INSERT INTO league_manager.player VALUES (281, 374508, NULL, 'SaveTheTrees', false, 27, NULL);
INSERT INTO league_manager.player VALUES (282, 763263, NULL, 'PMA Advisor', false, 27, NULL);
INSERT INTO league_manager.player VALUES (283, 634712, NULL, 'PJ', false, 27, NULL);
INSERT INTO league_manager.player VALUES (284, 634696, NULL, 'Ned', false, 27, NULL);
INSERT INTO league_manager.player VALUES (285, 469753, NULL, 'Malfunction', false, 27, NULL);
INSERT INTO league_manager.player VALUES (286, 469752, NULL, 'ginjaninja', false, 27, NULL);
INSERT INTO league_manager.player VALUES (287, 746897, NULL, 'Djdestroyer', false, 27, NULL);
INSERT INTO league_manager.player VALUES (288, 108676, NULL, 'raln', false, 29, NULL);
INSERT INTO league_manager.player VALUES (289, NULL, NULL, 'INELL', false, 29, NULL);
INSERT INTO league_manager.player VALUES (290, 781822, NULL, 'Pav', false, 29, NULL);
INSERT INTO league_manager.player VALUES (291, 733038, NULL, 'nikki', false, 30, NULL);
INSERT INTO league_manager.player VALUES (292, 334964, NULL, 'Razz', false, 30, NULL);
INSERT INTO league_manager.player VALUES (293, NULL, NULL, 'yabo', false, 32, NULL);
INSERT INTO league_manager.player VALUES (294, 830525, NULL, 'Corzo', false, 32, NULL);
INSERT INTO league_manager.player VALUES (295, 215850, NULL, 'Mudlee', false, 32, NULL);
INSERT INTO league_manager.player VALUES (296, 841274, NULL, 'Ryan', false, 33, NULL);
INSERT INTO league_manager.player VALUES (297, 1006589, NULL, 'tomato', false, 33, NULL);
INSERT INTO league_manager.player VALUES (298, 575, NULL, 'BobTooGood', false, 33, NULL);
INSERT INTO league_manager.player VALUES (299, 6267, NULL, 'Son', false, 33, NULL);
INSERT INTO league_manager.player VALUES (300, 888661, NULL, 'pandaleet', false, 33, NULL);
INSERT INTO league_manager.player VALUES (301, 968569, NULL, 'bazooka_cz', false, 33, NULL);
INSERT INTO league_manager.player VALUES (302, 936632, NULL, 'Brodie22', false, 33, NULL);
INSERT INTO league_manager.player VALUES (303, 807469, NULL, 'Sulx', false, 33, NULL);
INSERT INTO league_manager.player VALUES (304, 480254, NULL, 'Rocky', false, 33, NULL);
INSERT INTO league_manager.player VALUES (305, 473745, NULL, 'Zapdis', false, 33, NULL);
INSERT INTO league_manager.player VALUES (306, 851143, NULL, 'benny.', false, 33, NULL);
INSERT INTO league_manager.player VALUES (307, 880736, NULL, 'Larry', false, 33, NULL);
INSERT INTO league_manager.player VALUES (308, 918088, NULL, 'Liebe', false, 33, NULL);
INSERT INTO league_manager.player VALUES (309, 610442, NULL, 'Pogba', false, 33, NULL);
INSERT INTO league_manager.player VALUES (310, 927642, NULL, 'DarwinNunez', false, 33, NULL);
INSERT INTO league_manager.player VALUES (311, 927618, NULL, 'Alecc', false, 33, NULL);
INSERT INTO league_manager.player VALUES (312, 927113, NULL, 'orang', false, 33, NULL);
INSERT INTO league_manager.player VALUES (313, 935509, NULL, 'kaidan', false, 33, NULL);
INSERT INTO league_manager.player VALUES (314, 935508, NULL, 'Sue Rao', false, 33, NULL);
INSERT INTO league_manager.player VALUES (315, 386493, NULL, 'wizmid', false, 33, NULL);
INSERT INTO league_manager.player VALUES (316, 387542, NULL, 'aytreena', false, 33, NULL);
INSERT INTO league_manager.player VALUES (317, 961867, NULL, 'Beanos', false, 33, NULL);
INSERT INTO league_manager.player VALUES (318, 968600, NULL, 'Fishy', false, 33, NULL);
INSERT INTO league_manager.player VALUES (319, 956671, NULL, 'GGUDJ', false, 33, NULL);
INSERT INTO league_manager.player VALUES (320, 956675, NULL, 'THEJAMES', false, 33, NULL);
INSERT INTO league_manager.player VALUES (321, 1127081, NULL, 'TaserTaser', false, 33, NULL);
INSERT INTO league_manager.player VALUES (322, 485426, NULL, 'cheeky', false, 33, NULL);
INSERT INTO league_manager.player VALUES (323, 880323, NULL, 'baz', false, 33, NULL);
INSERT INTO league_manager.player VALUES (324, 1207020, NULL, 'midside', false, 36, NULL);
INSERT INTO league_manager.player VALUES (325, 779865, NULL, 'Blazendy', false, 36, NULL);
INSERT INTO league_manager.player VALUES (326, 1085421, NULL, 'ARC-5555 Fives', false, 36, NULL);
INSERT INTO league_manager.player VALUES (327, 735366, NULL, 'halios_', false, 36, NULL);
INSERT INTO league_manager.player VALUES (328, 1004826, NULL, 'willzz', false, 36, NULL);
INSERT INTO league_manager.player VALUES (329, 1132645, NULL, 'skeezy', false, 36, NULL);
INSERT INTO league_manager.player VALUES (330, 1014458, NULL, 'joshy8348', false, 36, NULL);
INSERT INTO league_manager.player VALUES (331, 1167885, NULL, 'jstris', false, 36, NULL);
INSERT INTO league_manager.player VALUES (332, 1167886, NULL, 'hogfrog', false, 36, NULL);
INSERT INTO league_manager.player VALUES (333, 1167884, NULL, 'keoa', false, 36, NULL);
INSERT INTO league_manager.player VALUES (334, 1167888, NULL, 'whipee', false, 36, NULL);
INSERT INTO league_manager.player VALUES (335, 1085317, NULL, 'Dwarf', false, 36, NULL);
INSERT INTO league_manager.player VALUES (336, 660936, NULL, 'Jacko', false, 36, NULL);
INSERT INTO league_manager.player VALUES (337, 1278149, NULL, 'Lausiie', false, 38, NULL);
INSERT INTO league_manager.player VALUES (338, 552377, NULL, 'Pluto', false, 39, NULL);
INSERT INTO league_manager.player VALUES (339, 462563, NULL, 'gecko', false, 39, NULL);
INSERT INTO league_manager.player VALUES (340, 279331, NULL, 'Stuba', false, 39, NULL);
INSERT INTO league_manager.player VALUES (341, 462545, NULL, 'Ratinson', false, 39, NULL);
INSERT INTO league_manager.player VALUES (342, 944130, NULL, 'Oak', false, 39, NULL);
INSERT INTO league_manager.player VALUES (343, 1243647, NULL, 'zenonix', false, 39, NULL);
INSERT INTO league_manager.player VALUES (344, 231086, NULL, 'zuza', false, 39, NULL);
INSERT INTO league_manager.player VALUES (345, 295085, NULL, 'true23', false, 39, NULL);
INSERT INTO league_manager.player VALUES (346, 949392, NULL, 'lcr', false, 39, NULL);
INSERT INTO league_manager.player VALUES (347, 949426, NULL, 'mitchb', false, 39, NULL);
INSERT INTO league_manager.player VALUES (348, 774099, NULL, 'don', false, 39, NULL);
INSERT INTO league_manager.player VALUES (349, 747983, NULL, 'Bogg', false, 39, NULL);
INSERT INTO league_manager.player VALUES (350, 1128923, NULL, 'Anthony', false, 39, NULL);
INSERT INTO league_manager.player VALUES (351, 717352, NULL, 'sooshi', false, 39, NULL);
INSERT INTO league_manager.player VALUES (352, 742828, NULL, 'ScAr', false, 39, NULL);
INSERT INTO league_manager.player VALUES (353, 1225714, NULL, 'luca', false, 39, NULL);
INSERT INTO league_manager.player VALUES (354, 1136451, NULL, 'spooder', false, 39, NULL);
INSERT INTO league_manager.player VALUES (356, 285238, NULL, 'Warchook', false, 39, NULL);
INSERT INTO league_manager.player VALUES (357, 866634, NULL, 'silly13sausage', false, 39, NULL);
INSERT INTO league_manager.player VALUES (358, 872566, NULL, 'Frozt', false, 39, NULL);
INSERT INTO league_manager.player VALUES (359, 874212, NULL, 'LilToddie', false, 39, NULL);
INSERT INTO league_manager.player VALUES (360, 872679, NULL, 'oozenada', false, 39, NULL);
INSERT INTO league_manager.player VALUES (361, 1133151, NULL, 'Kix', false, 39, NULL);
INSERT INTO league_manager.player VALUES (362, 1041875, NULL, 'Gibbo', false, 39, NULL);
INSERT INTO league_manager.player VALUES (363, 785776, NULL, 'RUKUS', false, 39, NULL);
INSERT INTO league_manager.player VALUES (364, NULL, NULL, 'Valley', false, 11, NULL);
INSERT INTO league_manager.player VALUES (365, NULL, NULL, 'TiltedWilts', false, 11, NULL);
INSERT INTO league_manager.player VALUES (366, NULL, NULL, 'Chrubby', false, 11, NULL);
INSERT INTO league_manager.player VALUES (367, NULL, NULL, '0mni', false, 11, NULL);
INSERT INTO league_manager.player VALUES (368, NULL, NULL, 'Tomysax', false, 11, NULL);
INSERT INTO league_manager.player VALUES (369, NULL, NULL, 'fish fear me', false, 11, NULL);
INSERT INTO league_manager.player VALUES (370, NULL, NULL, 'Bullit	', false, 11, NULL);
INSERT INTO league_manager.player VALUES (371, NULL, NULL, 'Glyphids fear me', false, 11, NULL);
INSERT INTO league_manager.player VALUES (372, NULL, NULL, 'Kosovo', false, 11, NULL);
INSERT INTO league_manager.player VALUES (373, NULL, NULL, 'IndovaaDiff', false, 11, NULL);
INSERT INTO league_manager.player VALUES (374, NULL, NULL, 'fjordnoit', false, 11, NULL);
INSERT INTO league_manager.player VALUES (375, NULL, NULL, 'dandamanlol', false, 11, NULL);
INSERT INTO league_manager.player VALUES (376, NULL, NULL, 'Carch', false, 11, NULL);
INSERT INTO league_manager.player VALUES (377, NULL, NULL, 'Watto', false, 11, NULL);
INSERT INTO league_manager.player VALUES (378, NULL, NULL, 'bailey', false, 11, NULL);
INSERT INTO league_manager.player VALUES (379, NULL, NULL, 'Gerofied	', false, 11, NULL);
INSERT INTO league_manager.player VALUES (380, NULL, NULL, 'Magic_Mc_Nugget	', false, 11, NULL);
INSERT INTO league_manager.player VALUES (381, NULL, NULL, 'Sparky', false, 11, NULL);
INSERT INTO league_manager.player VALUES (382, 142568, NULL, 'Lloyd', false, 22, NULL);
INSERT INTO league_manager.player VALUES (383, 209703, NULL, 'age', false, 22, NULL);
INSERT INTO league_manager.player VALUES (384, 465278, NULL, 'Ohlai', false, 22, NULL);
INSERT INTO league_manager.player VALUES (385, 804811, NULL, 'Willack', false, 33, NULL);
INSERT INTO league_manager.player VALUES (386, 877015, NULL, 's4m', false, 33, NULL);
INSERT INTO league_manager.player VALUES (355, 1322560, 2, 'Haelnorr', false, 39, NULL);


--
-- TOC entry 3424 (class 0 OID 21091)
-- Dependencies: 252
-- Data for Name: player_award; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3443 (class 0 OID 21281)
-- Dependencies: 271
-- Data for Name: player_match_data; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3426 (class 0 OID 21114)
-- Dependencies: 254
-- Data for Name: player_team; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.player_team VALUES (8, 50, 105, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (9, 51, 105, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (10, 52, 105, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (11, 53, 105, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (12, 247, 3, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (13, 175, 3, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (14, 171, 3, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (15, 246, 3, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (16, 339, 242, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (17, 338, 242, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (18, 341, 242, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (19, 340, 242, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (20, 150, 4, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (21, 156, 4, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (22, 84, 4, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (23, 288, 5, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (24, 221, 5, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (25, 290, 5, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (26, 220, 5, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (27, 289, 5, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (28, 327, 206, '2023-08-28 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (29, 326, 206, '2023-08-28 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (30, 328, 206, '2023-08-28 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (31, 337, 206, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (32, 308, 206, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (33, 382, 6, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (34, 258, 6, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (35, 268, 6, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (36, 257, 6, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (37, 256, 6, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (38, 259, 6, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (39, 1, 74, '2019-03-30 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (40, 2, 74, '2019-03-30 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (41, 3, 74, '2019-03-30 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (42, 4, 74, '2019-03-30 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (43, 5, 74, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (44, 22, 74, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (45, 23, 74, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (46, 2, 74, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (47, 1, 74, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (48, 54, 74, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (49, 3, 74, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (50, 251, 181, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (51, 255, 181, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (52, 226, 181, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (53, 90, 181, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (54, 228, 181, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (55, 48, 181, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (56, 6, 75, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (57, 7, 75, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (58, 8, 75, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (59, 9, 75, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (60, 10, 75, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (61, 11, 75, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (62, 99, 262, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (63, 100, 262, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (64, 72, 262, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (65, 101, 262, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (66, 12, 13, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (67, 13, 13, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (68, 14, 13, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (69, 15, 13, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (70, 16, 13, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (71, 12, 13, '2020-08-17 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (72, 13, 13, '2020-08-17 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (73, 121, 13, '2020-08-17 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (74, 122, 13, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (75, 151, 13, '2021-02-15 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (76, 166, 13, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (77, 177, 13, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (78, 12, 13, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (79, 13, 13, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (80, 383, 13, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (81, 121, 13, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (82, 324, 13, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (83, 12, 13, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (84, 13, 13, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (85, 348, 13, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (86, 121, 13, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (87, 250, 200, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (88, 261, 200, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (89, 294, 200, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (90, 251, 200, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (91, 21, 81, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (92, 27, 81, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (93, 38, 81, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (94, 24, 81, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (95, 159, 182, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (96, 48, 182, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (97, 38, 182, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (98, 12, 182, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (99, 13, 182, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (100, 268, 10, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (101, 258, 10, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (102, 159, 10, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (103, 257, 10, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (104, 256, 10, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (105, 260, 11, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (106, 116, 11, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (107, 175, 11, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (108, 158, 11, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (109, 119, 11, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (110, 147, 11, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (111, 84, 11, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (112, 357, 248, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (113, 358, 248, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (114, 360, 248, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (115, 359, 248, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (116, 304, 185, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (117, 303, 185, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (118, 302, 185, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (119, 157, 238, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (120, 119, 238, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (121, 156, 238, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (122, 207, 238, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (123, 54, 238, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (124, 158, 14, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (125, 157, 14, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (126, 156, 14, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (127, 90, 8, '2020-11-23 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (128, 18, 8, '2020-11-23 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (129, 19, 8, '2020-11-23 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (130, 19, 8, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (131, 90, 8, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (132, 18, 8, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (133, 163, 8, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (134, 346, 244, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (135, 345, 244, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (136, 347, 244, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (137, 19, 12, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (138, 163, 12, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (139, 18, 12, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (140, 82, 12, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (141, 157, 175, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (142, 202, 175, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (143, 261, 175, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (144, 156, 175, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (145, 250, 175, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (146, 112, 265, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (147, 118, 265, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (148, 123, 265, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (149, 124, 265, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (150, 183, 15, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (151, 185, 15, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (152, 184, 15, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (153, 186, 15, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (154, 182, 15, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (155, 184, 15, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (156, 186, 15, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (157, 224, 15, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (158, 183, 15, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (159, 48, 247, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (160, 355, 247, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (161, 356, 247, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (162, 54, 249, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (163, 119, 249, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (164, 128, 249, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (165, 308, 186, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (166, 306, 186, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (167, 305, 186, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (168, 307, 186, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (169, 309, 186, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (170, 1, 80, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (171, 3, 80, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (172, 46, 80, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (173, 13, 80, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (174, 42, 80, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (175, 30, 80, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (176, 312, 187, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (177, 310, 187, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (178, 311, 187, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (179, 52, 19, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (180, 50, 19, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (181, 1, 19, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (182, 79, 19, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (183, 28, 19, '2020-08-17 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (184, 137, 19, '2020-11-23 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (185, 55, 19, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (186, 51, 19, '2020-05-25 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (187, 154, 19, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (188, 159, 19, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (189, 175, 19, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (190, 119, 19, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (191, 76, 19, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (192, 28, 19, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (193, 51, 19, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (194, 54, 19, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (195, 246, 19, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (196, 127, 19, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (197, 28, 19, '2023-08-28 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (198, 127, 19, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (199, 147, 19, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (200, 51, 19, '2023-08-28 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (201, 154, 19, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (202, 158, 19, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (203, 254, 19, '2024-01-14 00:00:00', '2024-03-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (204, 282, 19, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (205, 207, 203, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (206, 171, 203, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (207, 197, 203, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (208, 198, 17, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (209, 197, 17, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (210, 226, 17, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (211, 260, 17, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (212, 195, 17, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (213, 197, 18, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (214, 198, 18, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (215, 207, 18, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (216, 195, 18, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (217, 196, 18, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (218, 196, 20, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (219, 197, 20, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (220, 195, 20, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (221, 198, 20, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (222, 197, 21, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (223, 260, 21, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (224, 226, 21, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (225, 198, 21, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (226, 228, 21, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (227, 157, 113, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (228, 156, 113, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (229, 261, 113, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (230, 202, 113, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (231, 201, 22, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (232, 200, 22, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (233, 199, 22, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (234, 174, 22, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (235, 71, 254, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (236, 89, 254, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (237, 48, 254, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (238, 13, 204, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (239, 12, 204, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (240, 324, 204, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (241, 121, 204, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (242, 250, 239, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (243, 251, 239, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (244, 294, 239, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (245, 306, 239, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (246, 308, 239, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (247, 204, 24, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (248, 248, 24, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (249, 249, 24, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (250, 207, 24, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (251, 204, 25, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (252, 271, 25, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (253, 54, 25, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (254, 1, 25, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (255, 202, 25, '2021-07-26 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (256, 203, 25, '2021-07-26 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (257, 205, 25, '2021-07-26 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (258, 248, 25, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (259, 13, 76, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (260, 24, 76, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (261, 25, 76, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (262, 12, 76, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (263, 26, 76, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (264, 54, 76, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (265, 48, 76, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (266, 2, 76, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (267, 25, 76, '2020-03-30 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (268, 70, 76, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (269, 74, 76, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (270, 38, 76, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (271, 44, 76, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (272, 246, 27, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (273, 247, 27, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (274, 175, 27, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (275, 184, 201, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (276, 186, 201, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (277, 224, 201, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (278, 150, 201, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (279, 28, 26, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (280, 247, 26, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (281, 246, 26, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (282, 250, 26, '2022-06-20 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (283, 251, 26, '2022-06-20 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (284, 157, 26, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (285, 268, 26, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (286, 18, 28, '2019-03-30 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (287, 19, 28, '2019-03-30 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (288, 20, 28, '2019-03-30 00:00:00', '2019-04-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (289, 21, 28, '2019-03-30 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (290, 48, 28, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (291, 25, 28, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (292, 26, 28, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (293, 44, 28, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (294, 28, 28, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (295, 18, 28, '2020-03-30 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (296, 17, 28, '2019-03-30 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (297, 21, 28, '2020-03-30 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (298, 84, 28, '2020-08-17 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (299, 125, 266, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (300, 126, 266, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (301, 127, 266, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (302, 82, 266, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (303, 364, 260, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (304, 365, 260, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (305, 366, 260, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (306, 367, 260, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (307, 368, 260, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (308, 161, 259, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (309, 151, 259, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (310, 72, 259, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (311, 147, 29, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (312, 150, 29, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (313, 84, 29, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (314, 17, 29, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (315, 178, 30, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (316, 179, 30, '2021-05-10 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (317, 180, 30, '2021-05-10 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (318, 181, 30, '2021-05-10 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (319, 206, 30, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (320, 55, 106, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (321, 26, 106, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (322, 56, 106, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (323, 57, 106, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (324, 58, 106, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (325, 79, 31, '2022-06-20 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (326, 147, 31, '2022-06-20 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (327, 17, 31, '2022-06-20 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (328, 84, 31, '2022-06-20 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (329, 1, 31, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (330, 207, 32, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (331, 135, 32, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (332, 273, 32, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (333, 272, 32, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (334, 274, 32, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (335, 85, 252, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (336, 54, 252, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (337, 86, 252, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (338, 59, 108, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (339, 60, 108, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (340, 61, 108, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (341, 207, 33, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (342, 208, 33, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (343, 209, 33, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (344, 164, 33, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (345, 175, 33, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (346, 28, 177, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (347, 150, 177, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (348, 158, 177, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (349, 51, 177, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (350, 250, 34, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (351, 251, 34, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (352, 90, 34, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (353, 157, 34, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (354, 351, 245, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (355, 349, 245, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (356, 329, 245, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (357, 350, 245, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (358, 226, 245, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (359, 135, 36, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (360, 162, 36, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (361, 127, 36, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (362, 137, 36, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (363, 159, 258, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (364, 369, 258, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (365, 370, 258, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (366, 371, 258, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (367, 372, 258, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (368, 162, 178, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (369, 205, 178, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (370, 135, 178, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (371, 280, 178, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (372, 192, 35, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (373, 127, 35, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (374, 253, 35, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (375, 191, 35, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (376, 252, 35, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (377, 160, 241, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (378, 335, 241, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (379, 313, 241, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (380, 319, 241, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (381, 261, 37, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (382, 162, 37, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (383, 270, 37, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (384, 164, 37, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (385, 275, 37, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (386, 248, 38, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (387, 186, 38, '2022-06-20 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (388, 224, 38, '2022-06-20 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (389, 184, 38, '2022-06-20 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (390, 183, 38, '2022-06-20 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (391, 261, 38, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (392, 276, 39, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (393, 277, 39, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (394, 278, 39, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (395, 313, 188, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (396, 314, 188, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (397, 316, 188, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (398, 315, 188, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (399, 135, 40, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (400, 1, 40, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (401, 76, 40, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (402, 137, 40, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (403, 130, 40, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (404, 102, 263, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (405, 103, 263, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (406, 104, 263, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (407, 105, 263, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (408, 106, 263, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (409, 261, 41, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (410, 164, 41, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (411, 262, 41, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (412, 270, 41, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (413, 269, 41, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (414, 269, 41, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (415, 164, 41, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (416, 262, 41, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (417, 270, 41, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (418, 128, 267, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (419, 129, 267, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (420, 130, 267, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (421, 131, 267, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (422, 132, 267, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (423, 211, 44, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (424, 212, 44, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (425, 210, 44, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (426, 213, 44, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (427, 197, 183, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (428, 294, 183, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (429, 257, 183, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (430, 258, 183, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (431, 268, 183, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (432, 226, 42, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (433, 228, 42, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (434, 384, 42, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (435, 27, 43, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (436, 28, 43, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (437, 29, 43, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (438, 30, 43, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (439, 31, 43, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (440, 32, 43, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (441, 28, 43, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (442, 55, 43, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (443, 147, 43, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (444, 125, 43, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (445, 90, 43, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (446, 246, 240, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (447, 254, 240, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (448, 147, 240, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (449, 130, 240, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (450, 172, 45, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (451, 254, 45, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (452, 228, 45, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (453, 163, 45, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (454, 255, 45, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (455, 228, 45, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (456, 254, 45, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (457, 171, 45, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (458, 246, 45, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (459, 172, 45, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (460, 255, 45, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (461, 163, 45, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (462, 385, 207, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (463, 352, 207, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (464, 330, 207, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (465, 329, 207, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (466, 386, 207, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (467, 62, 111, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (468, 63, 111, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (469, 64, 111, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (470, 65, 111, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (471, 66, 110, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (472, 67, 110, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (473, 68, 110, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (474, 69, 110, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (475, 288, 208, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (476, 222, 208, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (477, 220, 208, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (478, 223, 208, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (479, 214, 47, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (480, 215, 47, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (481, 216, 47, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (482, 217, 47, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (483, 202, 202, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (484, 119, 202, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (485, 157, 202, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (486, 54, 202, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (487, 76, 202, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (488, 111, 264, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (489, 107, 264, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (490, 108, 264, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (491, 109, 264, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (492, 110, 264, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (493, 133, 255, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (494, 134, 255, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (495, 135, 255, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (496, 218, 48, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (497, 219, 48, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (498, 220, 48, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (499, 221, 48, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (500, 79, 250, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (501, 74, 250, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (502, 125, 250, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (503, 127, 250, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (504, 70, 250, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (505, 127, 46, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (506, 125, 46, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (507, 154, 46, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (508, 159, 57, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (509, 157, 57, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (510, 162, 57, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (511, 156, 57, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (512, 150, 57, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (513, 167, 52, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (514, 169, 52, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (515, 96, 52, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (516, 168, 52, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (517, 165, 52, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (518, 76, 49, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (519, 160, 49, '2021-05-10 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (520, 76, 49, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (521, 119, 49, '2021-02-15 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (522, 1, 49, '2021-02-15 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (523, 54, 49, '2021-02-15 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (524, 88, 49, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (525, 331, 209, '2023-08-28 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (526, 332, 209, '2023-08-28 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (527, 334, 209, '2023-08-28 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (528, 333, 209, '2023-08-28 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (529, 202, 236, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (530, 162, 236, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (531, 135, 236, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (532, 84, 50, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (533, 171, 50, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (534, 172, 50, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (535, 170, 50, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (536, 172, 50, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (537, 171, 50, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (538, 170, 50, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (539, 321, 189, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (540, 318, 189, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (541, 317, 189, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (542, 319, 189, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (543, 320, 189, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (544, 336, 189, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (545, 335, 189, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (546, 113, 54, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (547, 280, 54, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (548, 279, 54, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (549, 281, 54, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (550, 282, 54, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (551, 159, 51, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (552, 113, 51, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (553, 201, 51, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (554, 1, 104, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (555, 70, 104, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (556, 71, 104, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (557, 3, 104, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (558, 72, 104, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (559, 33, 78, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (560, 34, 78, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (561, 35, 78, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (562, 36, 78, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (563, 37, 78, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (564, 197, 112, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (565, 258, 112, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (566, 268, 112, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (567, 257, 112, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (568, 226, 112, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (569, 73, 109, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (570, 42, 109, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (571, 74, 109, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (572, 75, 109, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (573, 112, 109, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (574, 84, 179, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (575, 254, 179, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (576, 260, 179, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (577, 246, 179, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (578, 306, 205, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (579, 313, 205, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (580, 322, 205, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (581, 283, 56, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (582, 284, 56, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (583, 286, 56, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (584, 285, 56, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (585, 287, 56, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (586, 267, 58, '2021-11-01 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (587, 265, 58, '2021-11-01 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (588, 263, 58, '2021-11-01 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (589, 264, 58, '2021-11-01 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (590, 266, 58, '2021-11-01 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (591, 159, 59, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (592, 24, 59, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (593, 155, 59, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (594, 90, 253, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (595, 119, 253, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (596, 88, 253, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (597, 76, 253, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (598, 83, 253, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (599, 133, 268, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (600, 102, 268, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (601, 101, 268, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (602, 134, 268, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (603, 135, 268, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (604, 117, 55, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (605, 115, 55, '2020-05-25 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (606, 114, 55, '2020-05-25 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (607, 136, 55, '2020-08-17 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (608, 161, 55, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (609, 160, 55, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (610, 116, 55, '2020-05-25 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (611, 113, 55, '2020-05-25 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (612, 3, 55, '2021-05-10 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (613, 79, 55, '2021-05-10 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (614, 80, 55, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (615, 160, 55, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (616, 161, 55, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (617, 116, 55, '2022-02-28 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (618, 90, 55, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (619, 127, 55, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (620, 171, 55, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (621, 113, 55, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (622, 207, 55, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (623, 270, 55, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (624, 282, 55, '2022-09-19 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (625, 116, 55, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (626, 282, 55, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (627, 113, 55, '2023-08-28 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (628, 172, 55, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (629, 325, 55, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (630, 197, 55, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (631, 258, 55, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (632, 76, 60, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (633, 137, 60, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (634, 135, 60, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (635, 17, 60, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (636, 130, 60, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (637, 162, 61, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (638, 157, 61, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (639, 156, 61, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (640, 158, 61, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (641, 248, 180, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (642, 113, 180, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (643, 119, 180, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (644, 147, 180, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (645, 127, 180, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (646, 55, 251, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (647, 130, 251, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (648, 76, 251, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (649, 1, 251, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (650, 88, 251, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (651, 373, 256, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (652, 374, 256, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (653, 375, 256, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (654, 376, 256, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (655, 377, 256, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (656, 137, 53, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (657, 138, 53, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (658, 72, 53, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (659, 139, 53, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (660, 170, 53, '2021-02-15 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (661, 150, 53, '2021-02-15 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (662, 171, 53, '2021-02-15 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (663, 172, 53, '2021-02-15 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (664, 167, 53, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (665, 128, 53, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (666, 137, 53, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (667, 130, 53, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (668, 193, 53, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (669, 137, 53, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (670, 128, 53, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (671, 130, 53, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (672, 291, 53, '2023-05-01 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (673, 330, 246, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (674, 352, 246, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (675, 353, 246, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (676, 354, 246, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (677, 142, 64, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (678, 143, 64, '2020-08-17 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (679, 381, 64, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (680, 140, 64, '2020-08-17 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (681, 141, 64, '2020-08-17 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (682, 144, 64, '2020-08-17 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (683, 153, 64, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (684, 24, 65, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (685, 187, 65, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (686, 188, 65, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (687, 174, 65, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (688, 189, 65, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (689, 159, 16, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (690, 158, 16, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (691, 224, 16, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (692, 221, 16, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (693, 17, 62, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (694, 127, 62, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (695, 135, 62, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (696, 28, 62, '2021-07-26 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (697, 242, 261, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (698, 378, 261, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (699, 241, 261, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (700, 244, 261, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (701, 186, 63, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (702, 184, 63, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (703, 182, 63, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (704, 183, 63, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (705, 185, 63, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (706, 186, 63, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (707, 184, 63, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (708, 162, 63, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (709, 183, 63, '2021-11-01 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (710, 184, 63, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (711, 186, 63, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (712, 248, 63, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (713, 224, 63, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (714, 150, 63, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (715, 127, 66, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (716, 192, 66, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (717, 190, 66, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (718, 191, 66, '2021-05-10 00:00:00', '2021-07-04 00:00:00');
INSERT INTO league_manager.player_team VALUES (719, 76, 67, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (720, 19, 67, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (721, 78, 67, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (722, 118, 67, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (723, 123, 67, '2020-05-25 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (724, 73, 67, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (725, 145, 67, '2020-08-17 00:00:00', '2020-10-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (726, 24, 67, '2020-03-30 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (727, 77, 67, '2020-03-30 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (728, 154, 67, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (729, 118, 67, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (730, 55, 67, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (731, 24, 67, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (732, 161, 67, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (733, 147, 67, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (734, 194, 67, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (735, 79, 68, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (736, 80, 68, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (737, 81, 68, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (738, 82, 68, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (739, 79, 68, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (740, 80, 68, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (741, 82, 68, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (742, 147, 70, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (743, 157, 70, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (744, 76, 70, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (745, 74, 70, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (746, 161, 70, '2021-11-01 00:00:00', '2022-01-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (747, 119, 7, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (748, 271, 7, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (749, 54, 7, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (750, 157, 7, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (751, 161, 7, '2022-06-20 00:00:00', '2022-08-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (752, 205, 114, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (753, 162, 114, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (754, 135, 114, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (755, 280, 114, '2023-01-16 00:00:00', '2023-03-12 00:00:00');
INSERT INTO league_manager.player_team VALUES (756, 162, 114, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (757, 205, 114, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (758, 135, 114, '2023-08-28 00:00:00', '2023-11-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (759, 197, 9, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (760, 257, 9, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (761, 258, 9, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (762, 226, 9, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (763, 195, 9, '2022-09-19 00:00:00', '2022-11-06 00:00:00');
INSERT INTO league_manager.player_team VALUES (764, 83, 102, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (765, 84, 102, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (766, 85, 102, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (767, 86, 102, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (768, 87, 102, '2020-03-30 00:00:00', '2020-07-25 00:00:00');
INSERT INTO league_manager.player_team VALUES (769, 28, 69, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (770, 158, 69, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (771, 221, 69, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (772, 224, 69, '2022-02-28 00:00:00', '2022-05-01 00:00:00');
INSERT INTO league_manager.player_team VALUES (773, 336, 243, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (774, 344, 243, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (775, 343, 243, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (776, 342, 243, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (777, 306, 243, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (778, 88, 103, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (779, 89, 103, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (780, 90, 103, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (781, 38, 103, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (782, 322, 176, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (783, 385, 176, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (784, 352, 176, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (785, 323, 176, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (786, 386, 176, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (787, 207, 184, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (788, 295, 184, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (789, 282, 184, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (790, 270, 184, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (791, 18, 184, '2023-05-01 00:00:00', '2023-07-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (792, 224, 237, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (793, 261, 237, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (794, 127, 237, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (795, 137, 237, '2024-01-14 00:00:00', NULL);
INSERT INTO league_manager.player_team VALUES (796, 222, 71, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (797, 224, 71, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (798, 223, 71, '2021-07-26 00:00:00', '2021-09-21 00:00:00');
INSERT INTO league_manager.player_team VALUES (799, 38, 77, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (800, 39, 77, '2019-05-18 00:00:00', '2019-06-30 00:00:00');
INSERT INTO league_manager.player_team VALUES (801, 2, 79, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (802, 28, 79, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (803, 18, 79, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (804, 31, 79, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (805, 12, 79, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (806, 49, 79, '2019-07-17 00:00:00', '2019-08-10 00:00:00');
INSERT INTO league_manager.player_team VALUES (807, 162, 72, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (808, 163, 72, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (809, 164, 72, '2021-02-15 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (810, 91, 107, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (811, 92, 107, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (812, 93, 107, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (813, 94, 107, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (814, 95, 107, '2020-03-30 00:00:00', '2020-05-16 00:00:00');
INSERT INTO league_manager.player_team VALUES (815, 146, 73, '2020-08-17 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (816, 147, 73, '2020-08-17 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (817, 3, 73, '2020-08-17 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (818, 85, 73, '2020-11-23 00:00:00', '2021-04-11 00:00:00');
INSERT INTO league_manager.player_team VALUES (819, 160, 257, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (820, 379, 257, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (821, 380, 257, '2020-11-23 00:00:00', '2021-01-17 00:00:00');
INSERT INTO league_manager.player_team VALUES (822, 148, 257, '2020-11-23 00:00:00', '2021-01-17 00:00:00');


--
-- TOC entry 3406 (class 0 OID 20896)
-- Dependencies: 234
-- Data for Name: season; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.season VALUES (1, 'Season 1', 'S1', 1, '2019-03-30', '2019-04-14', '2019-04-21', '2019-04-21', 1, false);
INSERT INTO league_manager.season VALUES (2, 'Season 2', 'S2', 1, '2019-05-18', '2019-06-23', '2019-06-29', '2019-06-30', 1, false);
INSERT INTO league_manager.season VALUES (3, 'Season 3', 'S3', 1, '2019-07-17', '2019-08-10', '2019-08-10', '2019-08-10', 1, false);
INSERT INTO league_manager.season VALUES (4, 'Season 4', 'S4', 1, '2020-03-30', '2020-05-03', '2020-05-04', '2020-05-16', 1, false);
INSERT INTO league_manager.season VALUES (5, 'Season 5', 'S5', 1, '2020-05-25', '2020-07-12', '2020-07-13', '2020-07-25', 1, false);
INSERT INTO league_manager.season VALUES (6, 'Season 6', 'S6', 1, '2020-08-17', '2020-10-11', '2020-10-12', '2020-10-25', 1, false);
INSERT INTO league_manager.season VALUES (7, 'Season 7', 'S7', 1, '2020-11-23', '2020-12-27', '2020-12-28', '2021-01-17', 1, false);
INSERT INTO league_manager.season VALUES (8, 'Season 8', 'S8', 1, '2021-02-15', '2021-03-21', '2021-03-22', '2021-04-11', 1, false);
INSERT INTO league_manager.season VALUES (9, 'Season 9', 'S9', 1, '2021-05-10', '2021-06-20', '2021-06-21', '2021-07-04', 1, false);
INSERT INTO league_manager.season VALUES (10, 'Season 10', 'S10', 1, '2021-07-26', '2021-09-05', '2021-09-06', '2021-09-21', 1, false);
INSERT INTO league_manager.season VALUES (11, 'Season 11', 'S11', 1, '2021-11-01', '2021-12-05', '2021-12-06', '2022-01-25', 1, false);
INSERT INTO league_manager.season VALUES (12, 'Season 12', 'S12', 1, '2022-02-28', '2022-04-03', '2022-04-04', '2022-05-01', 1, false);
INSERT INTO league_manager.season VALUES (13, 'Season 13', 'S13', 1, '2022-06-20', '2022-07-31', '2022-08-01', '2022-08-21', 1, false);
INSERT INTO league_manager.season VALUES (14, 'Season 14', 'S14', 1, '2022-09-19', '2022-10-30', '2022-10-31', '2022-11-06', 1, false);
INSERT INTO league_manager.season VALUES (15, 'Season 15', 'S15', 1, '2023-01-16', '2023-02-26', '2023-02-27', '2023-03-12', 1, false);
INSERT INTO league_manager.season VALUES (16, 'Season 16', 'S16', 1, '2023-05-01', '2023-06-11', '2023-06-12', '2023-07-17', 1, false);
INSERT INTO league_manager.season VALUES (17, 'Season 17', 'S17', 1, '2023-08-28', '2023-10-15', '2023-10-16', '2023-11-10', 1, false);
INSERT INTO league_manager.season VALUES (18, 'Season 18', 'S18', 1, '2024-01-14', '2024-02-25', '2024-02-26', '2024-03-25', 1, false);
INSERT INTO league_manager.season VALUES (19, 'Season 19', 'S19', 1, '2024-05-10', NULL, NULL, '2024-08-14', 1, true);
INSERT INTO league_manager.season VALUES (20, 'Draft Season 1', 'SD1', 1, NULL, NULL, NULL, NULL, 1, false);


--
-- TOC entry 3408 (class 0 OID 20915)
-- Dependencies: 236
-- Data for Name: season_division; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.season_division VALUES (1, 1, 4);
INSERT INTO league_manager.season_division VALUES (2, 2, 4);
INSERT INTO league_manager.season_division VALUES (3, 3, 4);
INSERT INTO league_manager.season_division VALUES (4, 4, 4);
INSERT INTO league_manager.season_division VALUES (5, 5, 1);
INSERT INTO league_manager.season_division VALUES (6, 5, 3);
INSERT INTO league_manager.season_division VALUES (7, 6, 1);
INSERT INTO league_manager.season_division VALUES (8, 6, 3);
INSERT INTO league_manager.season_division VALUES (9, 7, 1);
INSERT INTO league_manager.season_division VALUES (10, 7, 2);
INSERT INTO league_manager.season_division VALUES (11, 7, 3);
INSERT INTO league_manager.season_division VALUES (12, 20, 5);
INSERT INTO league_manager.season_division VALUES (13, 20, 6);
INSERT INTO league_manager.season_division VALUES (14, 8, 1);
INSERT INTO league_manager.season_division VALUES (15, 8, 2);
INSERT INTO league_manager.season_division VALUES (16, 8, 3);
INSERT INTO league_manager.season_division VALUES (17, 9, 1);
INSERT INTO league_manager.season_division VALUES (18, 9, 2);
INSERT INTO league_manager.season_division VALUES (19, 10, 1);
INSERT INTO league_manager.season_division VALUES (20, 10, 3);
INSERT INTO league_manager.season_division VALUES (21, 11, 1);
INSERT INTO league_manager.season_division VALUES (22, 11, 3);
INSERT INTO league_manager.season_division VALUES (23, 12, 1);
INSERT INTO league_manager.season_division VALUES (24, 12, 2);
INSERT INTO league_manager.season_division VALUES (25, 12, 3);
INSERT INTO league_manager.season_division VALUES (26, 13, 1);
INSERT INTO league_manager.season_division VALUES (27, 13, 2);
INSERT INTO league_manager.season_division VALUES (28, 14, 1);
INSERT INTO league_manager.season_division VALUES (29, 14, 2);
INSERT INTO league_manager.season_division VALUES (30, 15, 1);
INSERT INTO league_manager.season_division VALUES (31, 16, 1);
INSERT INTO league_manager.season_division VALUES (32, 16, 2);
INSERT INTO league_manager.season_division VALUES (33, 16, 3);
INSERT INTO league_manager.season_division VALUES (34, 17, 1);
INSERT INTO league_manager.season_division VALUES (35, 17, 2);
INSERT INTO league_manager.season_division VALUES (36, 17, 3);
INSERT INTO league_manager.season_division VALUES (37, 18, 1);
INSERT INTO league_manager.season_division VALUES (38, 18, 2);
INSERT INTO league_manager.season_division VALUES (39, 18, 3);


--
-- TOC entry 3414 (class 0 OID 20976)
-- Dependencies: 242
-- Data for Name: season_division_team; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.season_division_team VALUES (1, 1, 74);
INSERT INTO league_manager.season_division_team VALUES (2, 1, 75);
INSERT INTO league_manager.season_division_team VALUES (3, 1, 13);
INSERT INTO league_manager.season_division_team VALUES (4, 1, 28);
INSERT INTO league_manager.season_division_team VALUES (5, 2, 74);
INSERT INTO league_manager.season_division_team VALUES (6, 2, 76);
INSERT INTO league_manager.season_division_team VALUES (7, 2, 28);
INSERT INTO league_manager.season_division_team VALUES (8, 2, 43);
INSERT INTO league_manager.season_division_team VALUES (9, 2, 78);
INSERT INTO league_manager.season_division_team VALUES (10, 2, 77);
INSERT INTO league_manager.season_division_team VALUES (11, 3, 81);
INSERT INTO league_manager.season_division_team VALUES (12, 3, 80);
INSERT INTO league_manager.season_division_team VALUES (13, 3, 28);
INSERT INTO league_manager.season_division_team VALUES (14, 3, 79);
INSERT INTO league_manager.season_division_team VALUES (15, 4, 105);
INSERT INTO league_manager.season_division_team VALUES (16, 4, 76);
INSERT INTO league_manager.season_division_team VALUES (17, 4, 28);
INSERT INTO league_manager.season_division_team VALUES (18, 4, 106);
INSERT INTO league_manager.season_division_team VALUES (19, 4, 108);
INSERT INTO league_manager.season_division_team VALUES (20, 4, 111);
INSERT INTO league_manager.season_division_team VALUES (21, 4, 110);
INSERT INTO league_manager.season_division_team VALUES (22, 4, 104);
INSERT INTO league_manager.season_division_team VALUES (23, 4, 109);
INSERT INTO league_manager.season_division_team VALUES (24, 4, 67);
INSERT INTO league_manager.season_division_team VALUES (25, 4, 68);
INSERT INTO league_manager.season_division_team VALUES (26, 4, 102);
INSERT INTO league_manager.season_division_team VALUES (27, 4, 103);
INSERT INTO league_manager.season_division_team VALUES (28, 4, 107);
INSERT INTO league_manager.season_division_team VALUES (29, 6, 262);
INSERT INTO league_manager.season_division_team VALUES (30, 6, 106);
INSERT INTO league_manager.season_division_team VALUES (31, 6, 263);
INSERT INTO league_manager.season_division_team VALUES (32, 6, 264);
INSERT INTO league_manager.season_division_team VALUES (33, 6, 109);
INSERT INTO league_manager.season_division_team VALUES (34, 6, 55);
INSERT INTO league_manager.season_division_team VALUES (35, 6, 67);
INSERT INTO league_manager.season_division_team VALUES (36, 6, 68);
INSERT INTO league_manager.season_division_team VALUES (37, 8, 13);
INSERT INTO league_manager.season_division_team VALUES (38, 8, 265);
INSERT INTO league_manager.season_division_team VALUES (39, 8, 266);
INSERT INTO league_manager.season_division_team VALUES (40, 8, 267);
INSERT INTO league_manager.season_division_team VALUES (41, 8, 264);
INSERT INTO league_manager.season_division_team VALUES (42, 8, 268);
INSERT INTO league_manager.season_division_team VALUES (43, 8, 55);
INSERT INTO league_manager.season_division_team VALUES (44, 8, 53);
INSERT INTO league_manager.season_division_team VALUES (45, 8, 64);
INSERT INTO league_manager.season_division_team VALUES (46, 8, 67);
INSERT INTO league_manager.season_division_team VALUES (47, 8, 73);
INSERT INTO league_manager.season_division_team VALUES (48, 11, 13);
INSERT INTO league_manager.season_division_team VALUES (49, 11, 260);
INSERT INTO league_manager.season_division_team VALUES (50, 11, 258);
INSERT INTO league_manager.season_division_team VALUES (51, 11, 256);
INSERT INTO league_manager.season_division_team VALUES (52, 11, 64);
INSERT INTO league_manager.season_division_team VALUES (53, 11, 261);
INSERT INTO league_manager.season_division_team VALUES (54, 11, 257);
INSERT INTO league_manager.season_division_team VALUES (55, 5, 74);
INSERT INTO league_manager.season_division_team VALUES (56, 5, 19);
INSERT INTO league_manager.season_division_team VALUES (57, 5, 254);
INSERT INTO league_manager.season_division_team VALUES (58, 5, 76);
INSERT INTO league_manager.season_division_team VALUES (59, 5, 28);
INSERT INTO league_manager.season_division_team VALUES (60, 5, 253);
INSERT INTO league_manager.season_division_team VALUES (61, 5, 102);
INSERT INTO league_manager.season_division_team VALUES (62, 7, 19);
INSERT INTO league_manager.season_division_team VALUES (63, 7, 76);
INSERT INTO league_manager.season_division_team VALUES (64, 7, 28);
INSERT INTO league_manager.season_division_team VALUES (65, 7, 252);
INSERT INTO league_manager.season_division_team VALUES (66, 7, 253);
INSERT INTO league_manager.season_division_team VALUES (67, 9, 249);
INSERT INTO league_manager.season_division_team VALUES (68, 9, 28);
INSERT INTO league_manager.season_division_team VALUES (69, 9, 250);
INSERT INTO league_manager.season_division_team VALUES (70, 9, 251);
INSERT INTO league_manager.season_division_team VALUES (71, 9, 73);
INSERT INTO league_manager.season_division_team VALUES (72, 10, 8);
INSERT INTO league_manager.season_division_team VALUES (73, 10, 19);
INSERT INTO league_manager.season_division_team VALUES (74, 10, 259);
INSERT INTO league_manager.season_division_team VALUES (75, 10, 255);
INSERT INTO league_manager.season_division_team VALUES (76, 10, 55);
INSERT INTO league_manager.season_division_team VALUES (77, 10, 67);
INSERT INTO league_manager.season_division_team VALUES (78, 14, 19);
INSERT INTO league_manager.season_division_team VALUES (79, 14, 28);
INSERT INTO league_manager.season_division_team VALUES (80, 14, 46);
INSERT INTO league_manager.season_division_team VALUES (81, 14, 49);
INSERT INTO league_manager.season_division_team VALUES (82, 14, 73);
INSERT INTO league_manager.season_division_team VALUES (83, 15, 14);
INSERT INTO league_manager.season_division_team VALUES (84, 15, 8);
INSERT INTO league_manager.season_division_team VALUES (85, 15, 59);
INSERT INTO league_manager.season_division_team VALUES (86, 15, 55);
INSERT INTO league_manager.season_division_team VALUES (87, 15, 68);
INSERT INTO league_manager.season_division_team VALUES (88, 15, 72);
INSERT INTO league_manager.season_division_team VALUES (89, 16, 13);
INSERT INTO league_manager.season_division_team VALUES (90, 16, 52);
INSERT INTO league_manager.season_division_team VALUES (91, 16, 53);
INSERT INTO league_manager.season_division_team VALUES (92, 16, 64);
INSERT INTO league_manager.season_division_team VALUES (93, 17, 43);
INSERT INTO league_manager.season_division_team VALUES (94, 17, 49);
INSERT INTO league_manager.season_division_team VALUES (95, 17, 55);
INSERT INTO league_manager.season_division_team VALUES (96, 17, 60);
INSERT INTO league_manager.season_division_team VALUES (97, 17, 61);
INSERT INTO league_manager.season_division_team VALUES (98, 18, 13);
INSERT INTO league_manager.season_division_team VALUES (99, 18, 19);
INSERT INTO league_manager.season_division_team VALUES (100, 18, 30);
INSERT INTO league_manager.season_division_team VALUES (101, 18, 53);
INSERT INTO league_manager.season_division_team VALUES (102, 18, 65);
INSERT INTO league_manager.season_division_team VALUES (103, 18, 63);
INSERT INTO league_manager.season_division_team VALUES (104, 18, 66);
INSERT INTO league_manager.season_division_team VALUES (105, 19, 15);
INSERT INTO league_manager.season_division_team VALUES (106, 19, 57);
INSERT INTO league_manager.season_division_team VALUES (107, 19, 49);
INSERT INTO league_manager.season_division_team VALUES (108, 19, 50);
INSERT INTO league_manager.season_division_team VALUES (109, 19, 55);
INSERT INTO league_manager.season_division_team VALUES (110, 19, 53);
INSERT INTO league_manager.season_division_team VALUES (111, 19, 62);
INSERT INTO league_manager.season_division_team VALUES (112, 19, 67);
INSERT INTO league_manager.season_division_team VALUES (113, 20, 12);
INSERT INTO league_manager.season_division_team VALUES (114, 20, 20);
INSERT INTO league_manager.season_division_team VALUES (115, 20, 22);
INSERT INTO league_manager.season_division_team VALUES (116, 20, 25);
INSERT INTO league_manager.season_division_team VALUES (117, 20, 30);
INSERT INTO league_manager.season_division_team VALUES (118, 20, 33);
INSERT INTO league_manager.season_division_team VALUES (119, 20, 44);
INSERT INTO league_manager.season_division_team VALUES (120, 20, 47);
INSERT INTO league_manager.season_division_team VALUES (121, 20, 48);
INSERT INTO league_manager.season_division_team VALUES (122, 20, 71);
INSERT INTO league_manager.season_division_team VALUES (123, 21, 25);
INSERT INTO league_manager.season_division_team VALUES (124, 21, 49);
INSERT INTO league_manager.season_division_team VALUES (125, 21, 50);
INSERT INTO league_manager.season_division_team VALUES (126, 21, 55);
INSERT INTO league_manager.season_division_team VALUES (127, 21, 16);
INSERT INTO league_manager.season_division_team VALUES (128, 21, 62);
INSERT INTO league_manager.season_division_team VALUES (129, 21, 63);
INSERT INTO league_manager.season_division_team VALUES (130, 21, 70);
INSERT INTO league_manager.season_division_team VALUES (131, 21, 4);
INSERT INTO league_manager.season_division_team VALUES (132, 22, 6);
INSERT INTO league_manager.season_division_team VALUES (133, 22, 13);
INSERT INTO league_manager.season_division_team VALUES (134, 22, 8);
INSERT INTO league_manager.season_division_team VALUES (135, 22, 18);
INSERT INTO league_manager.season_division_team VALUES (136, 22, 24);
INSERT INTO league_manager.season_division_team VALUES (137, 22, 27);
INSERT INTO league_manager.season_division_team VALUES (138, 22, 41);
INSERT INTO league_manager.season_division_team VALUES (139, 22, 42);
INSERT INTO league_manager.season_division_team VALUES (140, 22, 47);
INSERT INTO league_manager.season_division_team VALUES (141, 22, 58);
INSERT INTO league_manager.season_division_team VALUES (142, 23, 24);
INSERT INTO league_manager.season_division_team VALUES (143, 23, 25);
INSERT INTO league_manager.season_division_team VALUES (144, 23, 29);
INSERT INTO league_manager.season_division_team VALUES (145, 23, 40);
INSERT INTO league_manager.season_division_team VALUES (146, 23, 55);
INSERT INTO league_manager.season_division_team VALUES (147, 23, 63);
INSERT INTO league_manager.season_division_team VALUES (148, 23, 69);
INSERT INTO league_manager.season_division_team VALUES (149, 24, 3);
INSERT INTO league_manager.season_division_team VALUES (150, 24, 24);
INSERT INTO league_manager.season_division_team VALUES (151, 24, 34);
INSERT INTO league_manager.season_division_team VALUES (152, 24, 35);
INSERT INTO league_manager.season_division_team VALUES (153, 24, 45);
INSERT INTO league_manager.season_division_team VALUES (154, 24, 51);
INSERT INTO league_manager.season_division_team VALUES (155, 25, 6);
INSERT INTO league_manager.season_division_team VALUES (156, 25, 17);
INSERT INTO league_manager.season_division_team VALUES (157, 25, 41);
INSERT INTO league_manager.season_division_team VALUES (158, 25, 58);
INSERT INTO league_manager.season_division_team VALUES (159, 26, 25);
INSERT INTO league_manager.season_division_team VALUES (160, 26, 31);
INSERT INTO league_manager.season_division_team VALUES (161, 26, 7);
INSERT INTO league_manager.season_division_team VALUES (162, 26, 38);
INSERT INTO league_manager.season_division_team VALUES (163, 26, 26);
INSERT INTO league_manager.season_division_team VALUES (164, 26, 55);
INSERT INTO league_manager.season_division_team VALUES (165, 27, 10);
INSERT INTO league_manager.season_division_team VALUES (166, 27, 21);
INSERT INTO league_manager.season_division_team VALUES (167, 27, 32);
INSERT INTO league_manager.season_division_team VALUES (168, 27, 37);
INSERT INTO league_manager.season_division_team VALUES (169, 27, 39);
INSERT INTO league_manager.season_division_team VALUES (170, 27, 54);
INSERT INTO league_manager.season_division_team VALUES (171, 27, 56);
INSERT INTO league_manager.season_division_team VALUES (172, 27, 58);
INSERT INTO league_manager.season_division_team VALUES (173, 28, 11);
INSERT INTO league_manager.season_division_team VALUES (174, 28, 19);
INSERT INTO league_manager.season_division_team VALUES (175, 28, 25);
INSERT INTO league_manager.season_division_team VALUES (176, 28, 26);
INSERT INTO league_manager.season_division_team VALUES (177, 28, 31);
INSERT INTO league_manager.season_division_team VALUES (178, 28, 36);
INSERT INTO league_manager.season_division_team VALUES (179, 28, 38);
INSERT INTO league_manager.season_division_team VALUES (180, 29, 5);
INSERT INTO league_manager.season_division_team VALUES (181, 29, 45);
INSERT INTO league_manager.season_division_team VALUES (182, 29, 55);
INSERT INTO league_manager.season_division_team VALUES (183, 29, 9);
INSERT INTO league_manager.season_division_team VALUES (184, 30, 11);
INSERT INTO league_manager.season_division_team VALUES (185, 30, 19);
INSERT INTO league_manager.season_division_team VALUES (186, 30, 113);
INSERT INTO league_manager.season_division_team VALUES (187, 30, 45);
INSERT INTO league_manager.season_division_team VALUES (188, 30, 112);
INSERT INTO league_manager.season_division_team VALUES (189, 30, 55);
INSERT INTO league_manager.season_division_team VALUES (190, 30, 63);
INSERT INTO league_manager.season_division_team VALUES (191, 30, 114);
INSERT INTO league_manager.season_division_team VALUES (192, 31, 175);
INSERT INTO league_manager.season_division_team VALUES (193, 31, 175);
INSERT INTO league_manager.season_division_team VALUES (194, 31, 177);
INSERT INTO league_manager.season_division_team VALUES (195, 31, 178);
INSERT INTO league_manager.season_division_team VALUES (196, 31, 179);
INSERT INTO league_manager.season_division_team VALUES (197, 31, 180);
INSERT INTO league_manager.season_division_team VALUES (198, 31, 53);
INSERT INTO league_manager.season_division_team VALUES (199, 32, 181);
INSERT INTO league_manager.season_division_team VALUES (200, 32, 182);
INSERT INTO league_manager.season_division_team VALUES (201, 32, 183);
INSERT INTO league_manager.season_division_team VALUES (202, 32, 50);
INSERT INTO league_manager.season_division_team VALUES (203, 32, 184);
INSERT INTO league_manager.season_division_team VALUES (204, 33, 185);
INSERT INTO league_manager.season_division_team VALUES (205, 33, 186);
INSERT INTO league_manager.season_division_team VALUES (206, 33, 187);
INSERT INTO league_manager.season_division_team VALUES (207, 33, 188);
INSERT INTO league_manager.season_division_team VALUES (208, 33, 189);
INSERT INTO league_manager.season_division_team VALUES (209, 33, 176);
INSERT INTO league_manager.season_division_team VALUES (210, 34, 200);
INSERT INTO league_manager.season_division_team VALUES (211, 34, 19);
INSERT INTO league_manager.season_division_team VALUES (212, 34, 201);
INSERT INTO league_manager.season_division_team VALUES (213, 34, 202);
INSERT INTO league_manager.season_division_team VALUES (214, 34, 179);
INSERT INTO league_manager.season_division_team VALUES (215, 34, 53);
INSERT INTO league_manager.season_division_team VALUES (216, 34, 114);
INSERT INTO league_manager.season_division_team VALUES (217, 35, 181);
INSERT INTO league_manager.season_division_team VALUES (218, 35, 203);
INSERT INTO league_manager.season_division_team VALUES (219, 35, 204);
INSERT INTO league_manager.season_division_team VALUES (220, 35, 205);
INSERT INTO league_manager.season_division_team VALUES (221, 35, 55);
INSERT INTO league_manager.season_division_team VALUES (222, 36, 206);
INSERT INTO league_manager.season_division_team VALUES (223, 36, 207);
INSERT INTO league_manager.season_division_team VALUES (224, 36, 208);
INSERT INTO league_manager.season_division_team VALUES (225, 36, 209);
INSERT INTO league_manager.season_division_team VALUES (226, 36, 189);
INSERT INTO league_manager.season_division_team VALUES (227, 37, 238);
INSERT INTO league_manager.season_division_team VALUES (228, 37, 239);
INSERT INTO league_manager.season_division_team VALUES (229, 37, 240);
INSERT INTO league_manager.season_division_team VALUES (230, 37, 236);
INSERT INTO league_manager.season_division_team VALUES (231, 37, 237);
INSERT INTO league_manager.season_division_team VALUES (232, 38, 206);
INSERT INTO league_manager.season_division_team VALUES (233, 38, 19);
INSERT INTO league_manager.season_division_team VALUES (234, 38, 241);
INSERT INTO league_manager.season_division_team VALUES (235, 38, 55);
INSERT INTO league_manager.season_division_team VALUES (236, 39, 242);
INSERT INTO league_manager.season_division_team VALUES (237, 39, 13);
INSERT INTO league_manager.season_division_team VALUES (238, 39, 248);
INSERT INTO league_manager.season_division_team VALUES (239, 39, 244);
INSERT INTO league_manager.season_division_team VALUES (240, 39, 247);
INSERT INTO league_manager.season_division_team VALUES (241, 39, 245);
INSERT INTO league_manager.season_division_team VALUES (242, 39, 41);
INSERT INTO league_manager.season_division_team VALUES (243, 39, 209);
INSERT INTO league_manager.season_division_team VALUES (244, 39, 246);
INSERT INTO league_manager.season_division_team VALUES (245, 39, 243);


--
-- TOC entry 3428 (class 0 OID 21132)
-- Dependencies: 256
-- Data for Name: season_registration; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3386 (class 0 OID 20756)
-- Dependencies: 214
-- Data for Name: server_region; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.server_region VALUES ('eu-west', 'Europe', 'Western Europe', 'UTC+0');
INSERT INTO league_manager.server_region VALUES ('na-central', 'NA Central', 'North America Central', 'UTC-6');
INSERT INTO league_manager.server_region VALUES ('na-east', 'NA East', 'North America East', 'UTC-4');
INSERT INTO league_manager.server_region VALUES ('na-west', 'NA West', 'North America West', 'UTC-7');
INSERT INTO league_manager.server_region VALUES ('oce-east', 'Oceania', 'Australia/NZ', 'UTC+10');


--
-- TOC entry 3388 (class 0 OID 20765)
-- Dependencies: 216
-- Data for Name: team; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.team VALUES (3, '100 Throws', '100', '9cd9e0', NULL, NULL);
INSERT INTO league_manager.team VALUES (4, '3 Sea Men', '3S', '20c4fa', NULL, NULL);
INSERT INTO league_manager.team VALUES (5, '5 MANES ON THE RAIN TRAIN', '5MR', '24107e', NULL, NULL);
INSERT INTO league_manager.team VALUES (6, 'AbluhHaters', 'AH', 'bb83f1', NULL, NULL);
INSERT INTO league_manager.team VALUES (7, 'The Unbannables', 'BAN', '197770', NULL, NULL);
INSERT INTO league_manager.team VALUES (8, 'Burgur Boys', 'BB', 'f14747', NULL, NULL);
INSERT INTO league_manager.team VALUES (9, 'TIACBDBHOTIACBDBHFS', 'BDH', 'a1b2c2', NULL, NULL);
INSERT INTO league_manager.team VALUES (10, 'BoppyHaters', 'BH', 'bb83f1', NULL, NULL);
INSERT INTO league_manager.team VALUES (11, 'Brecqhou Hockey Team', 'BHT', '1abc9c', NULL, NULL);
INSERT INTO league_manager.team VALUES (12, 'Business Penguins', 'BP', 'ff8400', NULL, NULL);
INSERT INTO league_manager.team VALUES (13, 'Bananashire', 'BS', 'f5e93c', NULL, NULL);
INSERT INTO league_manager.team VALUES (14, 'Bunnings Snag', 'BUNS', 'bb421f', NULL, NULL);
INSERT INTO league_manager.team VALUES (15, 'Canberra Creamery', 'CC', 'fce8b2', NULL, NULL);
INSERT INTO league_manager.team VALUES (16, 'The Chickens', 'CHI', '34a853', NULL, NULL);
INSERT INTO league_manager.team VALUES (17, 'Donda 2', 'D2', '76db6b', NULL, NULL);
INSERT INTO league_manager.team VALUES (18, 'Donda Deluxe', 'DD', '87e092', NULL, NULL);
INSERT INTO league_manager.team VALUES (19, 'Dixen Spiders', 'DS', '30cc71', NULL, NULL);
INSERT INTO league_manager.team VALUES (20, 'Donda When', 'DW', 'b6d7a8', NULL, NULL);
INSERT INTO league_manager.team VALUES (21, 'Donda When & The Big Slappas', 'DWA', '88e494', NULL, NULL);
INSERT INTO league_manager.team VALUES (22, 'Eazy Peazy', 'EP', '000000', NULL, NULL);
INSERT INTO league_manager.team VALUES (24, 'FPAcademy', 'FPA', 'f1c40f', NULL, NULL);
INSERT INTO league_manager.team VALUES (25, 'FPSlappas', 'FPS', 'fcc762', NULL, NULL);
INSERT INTO league_manager.team VALUES (26, 'Gooey Guzzlers', 'GG', '2ecc71', NULL, NULL);
INSERT INTO league_manager.team VALUES (27, 'Game of Throws', 'GOT', '9cd9e0', NULL, NULL);
INSERT INTO league_manager.team VALUES (28, 'Goon Squids', 'GS', '068067', NULL, NULL);
INSERT INTO league_manager.team VALUES (29, 'Hommes Hows', 'HH', '8d604a', NULL, NULL);
INSERT INTO league_manager.team VALUES (30, 'Hood Oos', 'HO', 'c2925a', NULL, NULL);
INSERT INTO league_manager.team VALUES (31, 'In Loving Memory of @Homme Trophy', 'HT', '8d604a', NULL, NULL);
INSERT INTO league_manager.team VALUES (32, 'Karaage Slappas', 'KS', 'b00b69', NULL, NULL);
INSERT INTO league_manager.team VALUES (33, 'Lightning McChopper', 'LMC', 'ff0000', NULL, NULL);
INSERT INTO league_manager.team VALUES (34, 'Massive Dumps', 'MD', 'a84300', NULL, NULL);
INSERT INTO league_manager.team VALUES (35, 'Milwaukee Pucks', 'MP', '38761d', NULL, NULL);
INSERT INTO league_manager.team VALUES (36, 'Max Prestige Lightskins', 'MPL', '5d3fd3', NULL, NULL);
INSERT INTO league_manager.team VALUES (37, 'nc', 'NC', 'ed953e', NULL, NULL);
INSERT INTO league_manager.team VALUES (38, 'nc academy', 'NCA', 'ed953e', NULL, NULL);
INSERT INTO league_manager.team VALUES (39, 'NN Clan Slapshot', 'NNS', 'e91e63', NULL, NULL);
INSERT INTO league_manager.team VALUES (40, 'OGAT', 'OG', '1f8b4c', NULL, NULL);
INSERT INTO league_manager.team VALUES (41, 'Peanut Butter', 'PB', 'c99a18', NULL, NULL);
INSERT INTO league_manager.team VALUES (42, 'phillip', 'PH', 'e10fff', NULL, NULL);
INSERT INTO league_manager.team VALUES (43, 'Picnic Junkies', 'PJ', '76a5af', NULL, NULL);
INSERT INTO league_manager.team VALUES (44, 'Peking Puck', 'PKP', '922a2a', NULL, NULL);
INSERT INTO league_manager.team VALUES (45, 'Post Pingers', 'PP', 'f18a8a', NULL, NULL);
INSERT INTO league_manager.team VALUES (46, 'Rolling Cones', 'RC', 'cccccc', NULL, NULL);
INSERT INTO league_manager.team VALUES (47, 'Rat Pack', 'RP', '6aa84f', NULL, NULL);
INSERT INTO league_manager.team VALUES (48, 'Rink Rats', 'RR', 'f1c232', NULL, NULL);
INSERT INTO league_manager.team VALUES (49, 'SeggsChamp', 'SC', '8527ec', NULL, NULL);
INSERT INTO league_manager.team VALUES (50, 'Shire Challengers', 'SCH', '8e59d0', NULL, NULL);
INSERT INTO league_manager.team VALUES (51, 'SIL Fraternity', 'SF', 'e43ef0', NULL, NULL);
INSERT INTO league_manager.team VALUES (52, 'Schweppes FC', 'SFC', 'bf9000', NULL, NULL);
INSERT INTO league_manager.team VALUES (53, 'Sydney Gafs', 'SG', '3d98ec', NULL, NULL);
INSERT INTO league_manager.team VALUES (54, 'SIL Academy', 'SIA', 'de8ef8', NULL, NULL);
INSERT INTO league_manager.team VALUES (55, 'Such Is Life', 'SIL', 'dd73ff', NULL, NULL);
INSERT INTO league_manager.team VALUES (56, 'Spinjutsu Masters', 'SJM', '71368a', NULL, NULL);
INSERT INTO league_manager.team VALUES (57, 'Sarge Mimpson', 'SM', '34a853', NULL, NULL);
INSERT INTO league_manager.team VALUES (58, 'Sprucoid Games', 'SPR', 'a53abd', NULL, NULL);
INSERT INTO league_manager.team VALUES (59, 'Stick Shifters', 'SS', 'cfe2f3', NULL, NULL);
INSERT INTO league_manager.team VALUES (60, 'Sugondez', 'SUG', 'e4e4e4', NULL, NULL);
INSERT INTO league_manager.team VALUES (61, 'Sugondez Academy', 'SUGA', '15ffb9', NULL, NULL);
INSERT INTO league_manager.team VALUES (62, 'The Chucklenuts', 'TC', '6b7dec', NULL, NULL);
INSERT INTO league_manager.team VALUES (63, 'The Cream Team', 'TCT', 'd2daa3', NULL, NULL);
INSERT INTO league_manager.team VALUES (64, 'TaxFraud', 'TF', '00ff00', NULL, NULL);
INSERT INTO league_manager.team VALUES (65, 'Team Monika', 'TM', '95d2eb', NULL, NULL);
INSERT INTO league_manager.team VALUES (66, 'The Mighty Cucks', 'TMC', '6b60e2', NULL, NULL);
INSERT INTO league_manager.team VALUES (67, 'The Mother Puckers', 'TMP', '95d2eb', NULL, NULL);
INSERT INTO league_manager.team VALUES (68, 'The Postmen', 'TP', '05cc05', NULL, NULL);
INSERT INTO league_manager.team VALUES (69, 'Tuna Sub Backwards', 'TSB', 'd366ad', NULL, NULL);
INSERT INTO league_manager.team VALUES (70, 'The Super Muscle Boys', 'TSM', 'e60b5b', NULL, NULL);
INSERT INTO league_manager.team VALUES (71, 'Whew Boys', 'WB', 'e60b5b', NULL, NULL);
INSERT INTO league_manager.team VALUES (72, 'Wrappers', 'WRAP', 'b53b60', NULL, NULL);
INSERT INTO league_manager.team VALUES (73, 'Zinga', 'ZING', 'f37021', NULL, NULL);
INSERT INTO league_manager.team VALUES (74, 'Adelaide Avalanche', 'AA', 'a4c2f4', NULL, NULL);
INSERT INTO league_manager.team VALUES (75, 'AH Gang', 'AHG', '76a5af', NULL, NULL);
INSERT INTO league_manager.team VALUES (76, 'Full Throttle Pacers', 'FTP', 'f6b26b', NULL, NULL);
INSERT INTO league_manager.team VALUES (77, 'Windy Wippersnappers', 'WW', '8e7cc3', NULL, NULL);
INSERT INTO league_manager.team VALUES (78, 'Slappy Dusters', 'SD', 'dd7e6b', NULL, NULL);
INSERT INTO league_manager.team VALUES (79, 'Worldstar Hip Hop', 'WSHH', 'dd7e6b', NULL, NULL);
INSERT INTO league_manager.team VALUES (80, 'Dangle Snipe Celly', 'DSC', 'b4a7d6', NULL, NULL);
INSERT INTO league_manager.team VALUES (81, 'Blue Line Bandits', 'BLB', 'a4c2f4', NULL, NULL);
INSERT INTO league_manager.team VALUES (102, 'Trash', 'TRA', 'e06666', NULL, NULL);
INSERT INTO league_manager.team VALUES (103, 'Wall Grinders', 'WG', 'ead1dc', NULL, NULL);
INSERT INTO league_manager.team VALUES (104, 'Simp City Slappers', 'SCS', 'df72df', NULL, NULL);
INSERT INTO league_manager.team VALUES (105, '10 Dixen Cider', '10DC', 'd9ead3', NULL, NULL);
INSERT INTO league_manager.team VALUES (106, 'IFC', 'IFC', 'ffd966', NULL, NULL);
INSERT INTO league_manager.team VALUES (107, 'Wuhan Bats', 'WUH', '6d9eeb', NULL, NULL);
INSERT INTO league_manager.team VALUES (108, 'Kermit Sewerside', 'KER', 'fff2cc', NULL, NULL);
INSERT INTO league_manager.team VALUES (109, 'Solar Bears', 'SB', 'b4a7d6', NULL, NULL);
INSERT INTO league_manager.team VALUES (110, 'Pussy Slappers', 'PS', 'ea9999', NULL, NULL);
INSERT INTO league_manager.team VALUES (111, 'Puck Puck Goose', 'PPG', 'f3f3f3', NULL, NULL);
INSERT INTO league_manager.team VALUES (112, 'Slaughter Gang CEOs', 'CEO', '674ea7', NULL, NULL);
INSERT INTO league_manager.team VALUES (113, 'Dou ma Devils', 'DMD', 'cc0000', NULL, NULL);
INSERT INTO league_manager.team VALUES (114, 'Thomas Shoubi', 'TS', '1bf2ac', NULL, NULL);
INSERT INTO league_manager.team VALUES (175, 'Cairns Cucumbers', 'CCU', '1f8b4c', NULL, NULL);
INSERT INTO league_manager.team VALUES (176, 'West Coast Warriors', 'WCW', 'd8bd4a', NULL, NULL);
INSERT INTO league_manager.team VALUES (177, 'Manus Island Stingrays', 'MIS', 'ad1457', NULL, NULL);
INSERT INTO league_manager.team VALUES (178, 'Melbourne Marshys', 'MM', '1bf2ac', NULL, NULL);
INSERT INTO league_manager.team VALUES (179, 'South Sydney Sugargliders', 'SSS', 'bdbdbd', NULL, NULL);
INSERT INTO league_manager.team VALUES (180, 'Suva SIL', 'SSIL', 'de8ef8', NULL, NULL);
INSERT INTO league_manager.team VALUES (181, 'Adelaide Saints', 'AS', 'f3f3f3', NULL, NULL);
INSERT INTO league_manager.team VALUES (182, 'Bondi Beaches', 'BOB', 'ffff00', NULL, NULL);
INSERT INTO league_manager.team VALUES (183, 'Perth Porcupines', 'PPO', 'e67e22', NULL, NULL);
INSERT INTO league_manager.team VALUES (184, 'West Melbourne Moles', 'WMM', 'dadd1e', NULL, NULL);
INSERT INTO league_manager.team VALUES (185, 'Broome Sweepers', 'BSW', '992d22', NULL, NULL);
INSERT INTO league_manager.team VALUES (186, 'Christchurch Cripsies', 'CHC', '4d51e0', NULL, NULL);
INSERT INTO league_manager.team VALUES (187, 'Darwin Spiders', 'DSP', '2ecc71', NULL, NULL);
INSERT INTO league_manager.team VALUES (188, 'North Melbourne Magpies', 'NMM', '464b4b', NULL, NULL);
INSERT INTO league_manager.team VALUES (189, 'Shires Finest', 'SHI', 'e74c3c', NULL, NULL);
INSERT INTO league_manager.team VALUES (200, 'BBC News', 'BBC', 'c27c0e', NULL, NULL);
INSERT INTO league_manager.team VALUES (201, 'GOG 64', 'GOG', 'c7952a', NULL, NULL);
INSERT INTO league_manager.team VALUES (202, 'Redline Redheart', 'REDH', 'ff0000', NULL, NULL);
INSERT INTO league_manager.team VALUES (203, 'Donda', 'DON', '990000', NULL, NULL);
INSERT INTO league_manager.team VALUES (204, 'Fatpoggers Bananashire', 'FB', 'f5e93c', NULL, NULL);
INSERT INTO league_manager.team VALUES (205, 'Spice Boys', 'SPB', 'c0df22', NULL, NULL);
INSERT INTO league_manager.team VALUES (206, '501st Legion', '501', '3d85c6', NULL, NULL);
INSERT INTO league_manager.team VALUES (207, 'Pub Punishers', 'PUB', '1abc9c', NULL, NULL);
INSERT INTO league_manager.team VALUES (208, 'RAIN TRAIN', 'RT', 'b4b63d', NULL, NULL);
INSERT INTO league_manager.team VALUES (209, 'SG Clan', 'SGC', 'cf8e8e', NULL, NULL);
INSERT INTO league_manager.team VALUES (236, 'Shadow Garden', 'SHG', '9900ff', NULL, NULL);
INSERT INTO league_manager.team VALUES (237, 'Wheel Wizards', 'WHW', 'ff9900', NULL, NULL);
INSERT INTO league_manager.team VALUES (238, 'Bucket of Soup', 'BOS', 'e06666', NULL, NULL);
INSERT INTO league_manager.team VALUES (239, 'Fizzy Fartboys', 'FF', 'fbbc04', NULL, NULL);
INSERT INTO league_manager.team VALUES (240, 'Ping Kings', 'PK', '22cd65', NULL, NULL);
INSERT INTO league_manager.team VALUES (241, 'Mucca Mad Boys', 'MMB', 'a61c00', NULL, NULL);
INSERT INTO league_manager.team VALUES (242, '2 Cousins 1 Friend', '2C1F', '3c78d8', NULL, NULL);
INSERT INTO league_manager.team VALUES (243, 'Vinegar Vipers', 'VV', '674ea7', NULL, NULL);
INSERT INTO league_manager.team VALUES (244, 'Burwood Council', 'BC', '38761d', NULL, NULL);
INSERT INTO league_manager.team VALUES (245, 'Massive Monkeys', 'MONK', 'ff00ff', NULL, NULL);
INSERT INTO league_manager.team VALUES (246, 'Taka co', 'TAKA', '00ff00', NULL, NULL);
INSERT INTO league_manager.team VALUES (247, 'CBR Milk', 'CBR', 'd6cccc', NULL, NULL);
INSERT INTO league_manager.team VALUES (248, 'BriteBombers', 'BRI', 'ff0000', NULL, NULL);
INSERT INTO league_manager.team VALUES (249, 'Cerberus', 'CER', '434343', NULL, NULL);
INSERT INTO league_manager.team VALUES (250, 'Robins', 'ROB', 'cccccc', NULL, NULL);
INSERT INTO league_manager.team VALUES (251, 'Sweepers', 'SWP', '29b3d6', NULL, NULL);
INSERT INTO league_manager.team VALUES (252, 'Keep It Steep', 'KIS', 'e06666', NULL, NULL);
INSERT INTO league_manager.team VALUES (253, 'Stompers', 'STOMP', '8e7cc3', NULL, NULL);
INSERT INTO league_manager.team VALUES (254, 'Fantastick', 'FANTA', 'f37021', NULL, NULL);
INSERT INTO league_manager.team VALUES (255, 'Rich Gang', 'RICH', 'f3f3f3', NULL, NULL);
INSERT INTO league_manager.team VALUES (256, 'Swiss Army Men', 'SAM', '4b8631', NULL, NULL);
INSERT INTO league_manager.team VALUES (257, 'Zinga Sliders', 'ZINGS', 'd58939', NULL, NULL);
INSERT INTO league_manager.team VALUES (258, 'McDonalds Management', 'MCD', 'cc0000', NULL, NULL);
INSERT INTO league_manager.team VALUES (259, 'HEY', 'HEY', 'c29231', NULL, NULL);
INSERT INTO league_manager.team VALUES (260, 'Hackey Racquets', 'HR', '8e7cc3', NULL, NULL);
INSERT INTO league_manager.team VALUES (261, 'The Cozzy Club', 'TCC', '4b93d5', NULL, NULL);
INSERT INTO league_manager.team VALUES (262, 'Baccy''s Simps', 'BACS', '4a86e8', NULL, NULL);
INSERT INTO league_manager.team VALUES (263, 'PASSSH', 'PASH', 'fcc762', NULL, NULL);
INSERT INTO league_manager.team VALUES (264, 'RiceFarming', 'RICE', 'a05151', NULL, NULL);
INSERT INTO league_manager.team VALUES (265, 'Canberra Bulls', 'BULLS', 'cc0000', NULL, NULL);
INSERT INTO league_manager.team VALUES (266, 'Gur Gurs Guardians', 'GUR', 'd58939', NULL, NULL);
INSERT INTO league_manager.team VALUES (267, 'Pegchamps', 'PEG', 'ffebb1', NULL, NULL);
INSERT INTO league_manager.team VALUES (268, 'Stompers Academy', 'STA', '8e7cc3', NULL, NULL);


--
-- TOC entry 3416 (class 0 OID 20994)
-- Dependencies: 244
-- Data for Name: team_award; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3430 (class 0 OID 21160)
-- Dependencies: 258
-- Data for Name: team_invites; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3400 (class 0 OID 20851)
-- Dependencies: 228
-- Data for Name: twitch; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--



--
-- TOC entry 3390 (class 0 OID 20775)
-- Dependencies: 218
-- Data for Name: user; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager."user" VALUES (2, 'Haelnorr', 'lockedonohoe@gmail.com', 'pbkdf2:sha256:260000$7yj7Ab92Y6eBbw1K$70990b46802f6757106c7cea6daaea13a4e0737bb11e394a890cd9b23d971369', false, '775ecd9c93bafa79fad5dbb6971aeb15', '2025-03-26 03:16:34', NULL);
INSERT INTO league_manager."user" VALUES (1, 'Admin', NULL, 'pbkdf2:sha256:260000$Cian1IQNTFaykz1A$92e9e244c5af13cbf5a2eb6933a571f48607932f2a16501859f3a893ee018686', false, '2ed61d5fae54a26e25f609711bcd6a6b', '2025-03-26 23:19:09', NULL);


--
-- TOC entry 3402 (class 0 OID 20865)
-- Dependencies: 230
-- Data for Name: user_permissions; Type: TABLE DATA; Schema: league_manager; Owner: postgres
--

INSERT INTO league_manager.user_permissions VALUES (1, 1, 1, NULL);
INSERT INTO league_manager.user_permissions VALUES (3, 2, 5, '247');
INSERT INTO league_manager.user_permissions VALUES (4, 2, 1, NULL);


--
-- TOC entry 3479 (class 0 OID 0)
-- Dependencies: 208
-- Name: award_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.award_id_seq', 1, false);


--
-- TOC entry 3480 (class 0 OID 0)
-- Dependencies: 219
-- Name: discord_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.discord_id_seq', 9, true);


--
-- TOC entry 3481 (class 0 OID 0)
-- Dependencies: 231
-- Name: division_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.division_id_seq', 6, true);


--
-- TOC entry 3482 (class 0 OID 0)
-- Dependencies: 221
-- Name: event_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.event_id_seq', 1, false);


--
-- TOC entry 3483 (class 0 OID 0)
-- Dependencies: 237
-- Name: final_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.final_id_seq', 1, false);


--
-- TOC entry 3484 (class 0 OID 0)
-- Dependencies: 245
-- Name: final_results_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.final_results_id_seq', 1, false);


--
-- TOC entry 3485 (class 0 OID 0)
-- Dependencies: 247
-- Name: free_agent_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.free_agent_id_seq', 119, true);


--
-- TOC entry 3486 (class 0 OID 0)
-- Dependencies: 223
-- Name: league_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.league_id_seq', 2, true);


--
-- TOC entry 3487 (class 0 OID 0)
-- Dependencies: 259
-- Name: lobby_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.lobby_id_seq', 1, false);


--
-- TOC entry 3488 (class 0 OID 0)
-- Dependencies: 261
-- Name: match_availability_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.match_availability_id_seq', 1, false);


--
-- TOC entry 3489 (class 0 OID 0)
-- Dependencies: 268
-- Name: match_data_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.match_data_id_seq', 1, false);


--
-- TOC entry 3490 (class 0 OID 0)
-- Dependencies: 249
-- Name: match_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.match_id_seq', 1, false);


--
-- TOC entry 3491 (class 0 OID 0)
-- Dependencies: 264
-- Name: match_review_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.match_review_id_seq', 1, false);


--
-- TOC entry 3492 (class 0 OID 0)
-- Dependencies: 266
-- Name: match_schedule_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.match_schedule_id_seq', 1, false);


--
-- TOC entry 3493 (class 0 OID 0)
-- Dependencies: 225
-- Name: matchtype_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.matchtype_id_seq', 3, true);


--
-- TOC entry 3494 (class 0 OID 0)
-- Dependencies: 212
-- Name: permission_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.permission_id_seq', 6, true);


--
-- TOC entry 3495 (class 0 OID 0)
-- Dependencies: 251
-- Name: player_award_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.player_award_id_seq', 1, false);


--
-- TOC entry 3496 (class 0 OID 0)
-- Dependencies: 239
-- Name: player_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.player_id_seq', 386, true);


--
-- TOC entry 3497 (class 0 OID 0)
-- Dependencies: 270
-- Name: player_match_data_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.player_match_data_id_seq', 1, false);


--
-- TOC entry 3498 (class 0 OID 0)
-- Dependencies: 253
-- Name: player_team_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.player_team_id_seq', 822, true);


--
-- TOC entry 3499 (class 0 OID 0)
-- Dependencies: 235
-- Name: season_division_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.season_division_id_seq', 40, true);


--
-- TOC entry 3500 (class 0 OID 0)
-- Dependencies: 241
-- Name: season_division_team_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.season_division_team_id_seq', 245, true);


--
-- TOC entry 3501 (class 0 OID 0)
-- Dependencies: 233
-- Name: season_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.season_id_seq', 20, true);


--
-- TOC entry 3502 (class 0 OID 0)
-- Dependencies: 255
-- Name: season_registration_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.season_registration_id_seq', 1, false);


--
-- TOC entry 3503 (class 0 OID 0)
-- Dependencies: 243
-- Name: team_award_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.team_award_id_seq', 1, false);


--
-- TOC entry 3504 (class 0 OID 0)
-- Dependencies: 215
-- Name: team_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.team_id_seq', 268, true);


--
-- TOC entry 3505 (class 0 OID 0)
-- Dependencies: 257
-- Name: team_invites_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.team_invites_id_seq', 1, false);


--
-- TOC entry 3506 (class 0 OID 0)
-- Dependencies: 227
-- Name: twitch_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.twitch_id_seq', 1, false);


--
-- TOC entry 3507 (class 0 OID 0)
-- Dependencies: 217
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.user_id_seq', 15, true);


--
-- TOC entry 3508 (class 0 OID 0)
-- Dependencies: 229
-- Name: user_permissions_id_seq; Type: SEQUENCE SET; Schema: league_manager; Owner: postgres
--

SELECT pg_catalog.setval('league_manager.user_permissions_id_seq', 4, true);


--
-- TOC entry 3095 (class 2606 OID 20723)
-- Name: arena arena_label_key; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.arena
    ADD CONSTRAINT arena_label_key UNIQUE (label);


--
-- TOC entry 3097 (class 2606 OID 20721)
-- Name: arena arena_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.arena
    ADD CONSTRAINT arena_pkey PRIMARY KEY (value);


--
-- TOC entry 3099 (class 2606 OID 20731)
-- Name: award award_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.award
    ADD CONSTRAINT award_pkey PRIMARY KEY (id);


--
-- TOC entry 3126 (class 2606 OID 20791)
-- Name: discord discord_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.discord
    ADD CONSTRAINT discord_pkey PRIMARY KEY (id);


--
-- TOC entry 3147 (class 2606 OID 20888)
-- Name: division division_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.division
    ADD CONSTRAINT division_pkey PRIMARY KEY (id);


--
-- TOC entry 3102 (class 2606 OID 20739)
-- Name: end_reason end_reason_label_key; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.end_reason
    ADD CONSTRAINT end_reason_label_key UNIQUE (label);


--
-- TOC entry 3104 (class 2606 OID 20737)
-- Name: end_reason end_reason_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.end_reason
    ADD CONSTRAINT end_reason_pkey PRIMARY KEY (value);


--
-- TOC entry 3129 (class 2606 OID 20805)
-- Name: event event_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (id);


--
-- TOC entry 3154 (class 2606 OID 20938)
-- Name: final final_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.final
    ADD CONSTRAINT final_pkey PRIMARY KEY (id);


--
-- TOC entry 3164 (class 2606 OID 21022)
-- Name: final_results final_results_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.final_results
    ADD CONSTRAINT final_results_pkey PRIMARY KEY (id);


--
-- TOC entry 3166 (class 2606 OID 21045)
-- Name: free_agent free_agent_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.free_agent
    ADD CONSTRAINT free_agent_pkey PRIMARY KEY (id);


--
-- TOC entry 3106 (class 2606 OID 20746)
-- Name: game_mode game_mode_label_key; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.game_mode
    ADD CONSTRAINT game_mode_label_key UNIQUE (label);


--
-- TOC entry 3108 (class 2606 OID 20744)
-- Name: game_mode game_mode_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.game_mode
    ADD CONSTRAINT game_mode_pkey PRIMARY KEY (value);


--
-- TOC entry 3134 (class 2606 OID 20822)
-- Name: league league_acronym_key; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.league
    ADD CONSTRAINT league_acronym_key UNIQUE (acronym);


--
-- TOC entry 3136 (class 2606 OID 20820)
-- Name: league league_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.league
    ADD CONSTRAINT league_pkey PRIMARY KEY (id);


--
-- TOC entry 3178 (class 2606 OID 21188)
-- Name: lobby lobby_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.lobby
    ADD CONSTRAINT lobby_pkey PRIMARY KEY (id);


--
-- TOC entry 3180 (class 2606 OID 21201)
-- Name: match_availability match_availability_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_availability
    ADD CONSTRAINT match_availability_pkey PRIMARY KEY (id);


--
-- TOC entry 3188 (class 2606 OID 21273)
-- Name: match_data match_data_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_data
    ADD CONSTRAINT match_data_pkey PRIMARY KEY (id);


--
-- TOC entry 3168 (class 2606 OID 21063)
-- Name: match match_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match
    ADD CONSTRAINT match_pkey PRIMARY KEY (id);


--
-- TOC entry 3182 (class 2606 OID 21216)
-- Name: match_result match_result_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_result
    ADD CONSTRAINT match_result_pkey PRIMARY KEY (id);


--
-- TOC entry 3184 (class 2606 OID 21242)
-- Name: match_review match_review_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_review
    ADD CONSTRAINT match_review_pkey PRIMARY KEY (id);


--
-- TOC entry 3186 (class 2606 OID 21260)
-- Name: match_schedule match_schedule_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_schedule
    ADD CONSTRAINT match_schedule_pkey PRIMARY KEY (id);


--
-- TOC entry 3138 (class 2606 OID 20838)
-- Name: matchtype matchtype_name_key; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.matchtype
    ADD CONSTRAINT matchtype_name_key UNIQUE (name);


--
-- TOC entry 3140 (class 2606 OID 20836)
-- Name: matchtype matchtype_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.matchtype
    ADD CONSTRAINT matchtype_pkey PRIMARY KEY (id);


--
-- TOC entry 3111 (class 2606 OID 20754)
-- Name: permission permission_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.permission
    ADD CONSTRAINT permission_pkey PRIMARY KEY (id);


--
-- TOC entry 3170 (class 2606 OID 21096)
-- Name: player_award player_award_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_award
    ADD CONSTRAINT player_award_pkey PRIMARY KEY (id);


--
-- TOC entry 3190 (class 2606 OID 21286)
-- Name: player_match_data player_match_data_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_match_data
    ADD CONSTRAINT player_match_data_pkey PRIMARY KEY (id);


--
-- TOC entry 3156 (class 2606 OID 20961)
-- Name: player player_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player
    ADD CONSTRAINT player_pkey PRIMARY KEY (id);


--
-- TOC entry 3158 (class 2606 OID 20963)
-- Name: player player_slap_id_key; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player
    ADD CONSTRAINT player_slap_id_key UNIQUE (slap_id);


--
-- TOC entry 3172 (class 2606 OID 21119)
-- Name: player_team player_team_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_team
    ADD CONSTRAINT player_team_pkey PRIMARY KEY (id);


--
-- TOC entry 3152 (class 2606 OID 20920)
-- Name: season_division season_division_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_division
    ADD CONSTRAINT season_division_pkey PRIMARY KEY (id);


--
-- TOC entry 3160 (class 2606 OID 20981)
-- Name: season_division_team season_division_team_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_division_team
    ADD CONSTRAINT season_division_team_pkey PRIMARY KEY (id);


--
-- TOC entry 3150 (class 2606 OID 20901)
-- Name: season season_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season
    ADD CONSTRAINT season_pkey PRIMARY KEY (id);


--
-- TOC entry 3174 (class 2606 OID 21137)
-- Name: season_registration season_registration_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_registration
    ADD CONSTRAINT season_registration_pkey PRIMARY KEY (id);


--
-- TOC entry 3113 (class 2606 OID 20762)
-- Name: server_region server_region_label_key; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.server_region
    ADD CONSTRAINT server_region_label_key UNIQUE (label);


--
-- TOC entry 3115 (class 2606 OID 20760)
-- Name: server_region server_region_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.server_region
    ADD CONSTRAINT server_region_pkey PRIMARY KEY (value);


--
-- TOC entry 3162 (class 2606 OID 20999)
-- Name: team_award team_award_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team_award
    ADD CONSTRAINT team_award_pkey PRIMARY KEY (id);


--
-- TOC entry 3176 (class 2606 OID 21165)
-- Name: team_invites team_invites_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team_invites
    ADD CONSTRAINT team_invites_pkey PRIMARY KEY (id);


--
-- TOC entry 3119 (class 2606 OID 20770)
-- Name: team team_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team
    ADD CONSTRAINT team_pkey PRIMARY KEY (id);


--
-- TOC entry 3143 (class 2606 OID 20856)
-- Name: twitch twitch_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.twitch
    ADD CONSTRAINT twitch_pkey PRIMARY KEY (id);


--
-- TOC entry 3145 (class 2606 OID 20870)
-- Name: user_permissions user_permissions_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.user_permissions
    ADD CONSTRAINT user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3124 (class 2606 OID 20780)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 3100 (class 1259 OID 20732)
-- Name: ix_league_manager_award_name; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE UNIQUE INDEX ix_league_manager_award_name ON league_manager.award USING btree (name);


--
-- TOC entry 3127 (class 1259 OID 20797)
-- Name: ix_league_manager_discord_discord_id; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE UNIQUE INDEX ix_league_manager_discord_discord_id ON league_manager.discord USING btree (discord_id);


--
-- TOC entry 3130 (class 1259 OID 20811)
-- Name: ix_league_manager_event_module; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE INDEX ix_league_manager_event_module ON league_manager.event USING btree (module);


--
-- TOC entry 3131 (class 1259 OID 20812)
-- Name: ix_league_manager_event_timestamp; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE INDEX ix_league_manager_event_timestamp ON league_manager.event USING btree ("timestamp");


--
-- TOC entry 3132 (class 1259 OID 20828)
-- Name: ix_league_manager_league_name; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE UNIQUE INDEX ix_league_manager_league_name ON league_manager.league USING btree (name);


--
-- TOC entry 3109 (class 1259 OID 20755)
-- Name: ix_league_manager_permission_key; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE UNIQUE INDEX ix_league_manager_permission_key ON league_manager.permission USING btree (key);


--
-- TOC entry 3148 (class 1259 OID 20912)
-- Name: ix_league_manager_season_name; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE INDEX ix_league_manager_season_name ON league_manager.season USING btree (name);


--
-- TOC entry 3116 (class 1259 OID 20771)
-- Name: ix_league_manager_team_acronym; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE UNIQUE INDEX ix_league_manager_team_acronym ON league_manager.team USING btree (acronym);


--
-- TOC entry 3117 (class 1259 OID 20772)
-- Name: ix_league_manager_team_name; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE UNIQUE INDEX ix_league_manager_team_name ON league_manager.team USING btree (name);


--
-- TOC entry 3141 (class 1259 OID 20862)
-- Name: ix_league_manager_twitch_twitch_id; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE UNIQUE INDEX ix_league_manager_twitch_twitch_id ON league_manager.twitch USING btree (twitch_id);


--
-- TOC entry 3120 (class 1259 OID 20781)
-- Name: ix_league_manager_user_email; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE UNIQUE INDEX ix_league_manager_user_email ON league_manager."user" USING btree (email);


--
-- TOC entry 3121 (class 1259 OID 20782)
-- Name: ix_league_manager_user_token; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE UNIQUE INDEX ix_league_manager_user_token ON league_manager."user" USING btree (token);


--
-- TOC entry 3122 (class 1259 OID 20783)
-- Name: ix_league_manager_user_username; Type: INDEX; Schema: league_manager; Owner: postgres
--

CREATE UNIQUE INDEX ix_league_manager_user_username ON league_manager."user" USING btree (username);


--
-- TOC entry 3191 (class 2606 OID 20792)
-- Name: discord discord_user_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.discord
    ADD CONSTRAINT discord_user_id_fkey FOREIGN KEY (user_id) REFERENCES league_manager."user"(id);


--
-- TOC entry 3199 (class 2606 OID 20889)
-- Name: division division_league_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.division
    ADD CONSTRAINT division_league_id_fkey FOREIGN KEY (league_id) REFERENCES league_manager.league(id);


--
-- TOC entry 3192 (class 2606 OID 20806)
-- Name: event event_user_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.event
    ADD CONSTRAINT event_user_id_fkey FOREIGN KEY (user_id) REFERENCES league_manager."user"(id);


--
-- TOC entry 3204 (class 2606 OID 20939)
-- Name: final final_away_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.final
    ADD CONSTRAINT final_away_team_id_fkey FOREIGN KEY (away_team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3205 (class 2606 OID 20944)
-- Name: final final_home_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.final
    ADD CONSTRAINT final_home_team_id_fkey FOREIGN KEY (home_team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3214 (class 2606 OID 21023)
-- Name: final_results final_results_final_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.final_results
    ADD CONSTRAINT final_results_final_id_fkey FOREIGN KEY (final_id) REFERENCES league_manager.final(id);


--
-- TOC entry 3215 (class 2606 OID 21028)
-- Name: final_results final_results_loser_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.final_results
    ADD CONSTRAINT final_results_loser_id_fkey FOREIGN KEY (loser_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3216 (class 2606 OID 21033)
-- Name: final_results final_results_winner_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.final_results
    ADD CONSTRAINT final_results_winner_id_fkey FOREIGN KEY (winner_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3206 (class 2606 OID 20949)
-- Name: final final_season_division_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.final
    ADD CONSTRAINT final_season_division_id_fkey FOREIGN KEY (season_division_id) REFERENCES league_manager.season_division(id);


--
-- TOC entry 3217 (class 2606 OID 21046)
-- Name: free_agent free_agent_player_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.free_agent
    ADD CONSTRAINT free_agent_player_id_fkey FOREIGN KEY (player_id) REFERENCES league_manager.player(id);


--
-- TOC entry 3218 (class 2606 OID 21051)
-- Name: free_agent free_agent_season_division_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.free_agent
    ADD CONSTRAINT free_agent_season_division_id_fkey FOREIGN KEY (season_division_id) REFERENCES league_manager.season_division(id);


--
-- TOC entry 3193 (class 2606 OID 20823)
-- Name: league league_server_region_value_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.league
    ADD CONSTRAINT league_server_region_value_fkey FOREIGN KEY (server_region_value) REFERENCES league_manager.server_region(value);


--
-- TOC entry 3236 (class 2606 OID 21189)
-- Name: lobby lobby_match_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.lobby
    ADD CONSTRAINT lobby_match_id_fkey FOREIGN KEY (match_id) REFERENCES league_manager.match(id);


--
-- TOC entry 3237 (class 2606 OID 21202)
-- Name: match_availability match_availability_match_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_availability
    ADD CONSTRAINT match_availability_match_id_fkey FOREIGN KEY (match_id) REFERENCES league_manager.match(id);


--
-- TOC entry 3238 (class 2606 OID 21207)
-- Name: match_availability match_availability_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_availability
    ADD CONSTRAINT match_availability_team_id_fkey FOREIGN KEY (team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3219 (class 2606 OID 21064)
-- Name: match match_away_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match
    ADD CONSTRAINT match_away_team_id_fkey FOREIGN KEY (away_team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3245 (class 2606 OID 21274)
-- Name: match_data match_data_lobby_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_data
    ADD CONSTRAINT match_data_lobby_id_fkey FOREIGN KEY (lobby_id) REFERENCES league_manager.lobby(id);


--
-- TOC entry 3220 (class 2606 OID 21069)
-- Name: match match_final_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match
    ADD CONSTRAINT match_final_id_fkey FOREIGN KEY (final_id) REFERENCES league_manager.final(id);


--
-- TOC entry 3221 (class 2606 OID 21074)
-- Name: match match_home_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match
    ADD CONSTRAINT match_home_team_id_fkey FOREIGN KEY (home_team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3239 (class 2606 OID 21217)
-- Name: match_result match_result_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_result
    ADD CONSTRAINT match_result_id_fkey FOREIGN KEY (id) REFERENCES league_manager.match(id);


--
-- TOC entry 3240 (class 2606 OID 21222)
-- Name: match_result match_result_loser_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_result
    ADD CONSTRAINT match_result_loser_id_fkey FOREIGN KEY (loser_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3241 (class 2606 OID 21227)
-- Name: match_result match_result_winner_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_result
    ADD CONSTRAINT match_result_winner_id_fkey FOREIGN KEY (winner_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3242 (class 2606 OID 21243)
-- Name: match_review match_review_match_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_review
    ADD CONSTRAINT match_review_match_id_fkey FOREIGN KEY (match_id) REFERENCES league_manager.match(id);


--
-- TOC entry 3243 (class 2606 OID 21248)
-- Name: match_review match_review_resolved_by_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_review
    ADD CONSTRAINT match_review_resolved_by_fkey FOREIGN KEY (resolved_by) REFERENCES league_manager."user"(id);


--
-- TOC entry 3244 (class 2606 OID 21261)
-- Name: match_schedule match_schedule_match_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match_schedule
    ADD CONSTRAINT match_schedule_match_id_fkey FOREIGN KEY (match_id) REFERENCES league_manager.match(id);


--
-- TOC entry 3222 (class 2606 OID 21079)
-- Name: match match_season_division_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match
    ADD CONSTRAINT match_season_division_id_fkey FOREIGN KEY (season_division_id) REFERENCES league_manager.season_division(id);


--
-- TOC entry 3223 (class 2606 OID 21084)
-- Name: match match_streamer_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.match
    ADD CONSTRAINT match_streamer_id_fkey FOREIGN KEY (streamer_id) REFERENCES league_manager."user"(id);


--
-- TOC entry 3194 (class 2606 OID 20839)
-- Name: matchtype matchtype_arena_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.matchtype
    ADD CONSTRAINT matchtype_arena_fkey FOREIGN KEY (arena) REFERENCES league_manager.arena(value);


--
-- TOC entry 3195 (class 2606 OID 20844)
-- Name: matchtype matchtype_game_mode_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.matchtype
    ADD CONSTRAINT matchtype_game_mode_fkey FOREIGN KEY (game_mode) REFERENCES league_manager.game_mode(value);


--
-- TOC entry 3224 (class 2606 OID 21097)
-- Name: player_award player_award_award_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_award
    ADD CONSTRAINT player_award_award_id_fkey FOREIGN KEY (award_id) REFERENCES league_manager.award(id);


--
-- TOC entry 3225 (class 2606 OID 21102)
-- Name: player_award player_award_player_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_award
    ADD CONSTRAINT player_award_player_id_fkey FOREIGN KEY (player_id) REFERENCES league_manager.player(id);


--
-- TOC entry 3226 (class 2606 OID 21107)
-- Name: player_award player_award_season_division_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_award
    ADD CONSTRAINT player_award_season_division_id_fkey FOREIGN KEY (season_division_id) REFERENCES league_manager.season_division(id);


--
-- TOC entry 3207 (class 2606 OID 20964)
-- Name: player player_first_season_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player
    ADD CONSTRAINT player_first_season_id_fkey FOREIGN KEY (first_season_id) REFERENCES league_manager.season_division(id);


--
-- TOC entry 3246 (class 2606 OID 21287)
-- Name: player_match_data player_match_data_match_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_match_data
    ADD CONSTRAINT player_match_data_match_id_fkey FOREIGN KEY (match_id) REFERENCES league_manager.match_data(id);


--
-- TOC entry 3247 (class 2606 OID 21292)
-- Name: player_match_data player_match_data_player_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_match_data
    ADD CONSTRAINT player_match_data_player_id_fkey FOREIGN KEY (player_id) REFERENCES league_manager.player(id);


--
-- TOC entry 3248 (class 2606 OID 21297)
-- Name: player_match_data player_match_data_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_match_data
    ADD CONSTRAINT player_match_data_team_id_fkey FOREIGN KEY (team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3227 (class 2606 OID 21120)
-- Name: player_team player_team_player_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_team
    ADD CONSTRAINT player_team_player_id_fkey FOREIGN KEY (player_id) REFERENCES league_manager.player(id);


--
-- TOC entry 3228 (class 2606 OID 21125)
-- Name: player_team player_team_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player_team
    ADD CONSTRAINT player_team_team_id_fkey FOREIGN KEY (team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3208 (class 2606 OID 20969)
-- Name: player player_user_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.player
    ADD CONSTRAINT player_user_id_fkey FOREIGN KEY (user_id) REFERENCES league_manager."user"(id);


--
-- TOC entry 3202 (class 2606 OID 20921)
-- Name: season_division season_division_division_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_division
    ADD CONSTRAINT season_division_division_id_fkey FOREIGN KEY (division_id) REFERENCES league_manager.division(id);


--
-- TOC entry 3203 (class 2606 OID 20926)
-- Name: season_division season_division_season_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_division
    ADD CONSTRAINT season_division_season_id_fkey FOREIGN KEY (season_id) REFERENCES league_manager.season(id);


--
-- TOC entry 3209 (class 2606 OID 20982)
-- Name: season_division_team season_division_team_season_division_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_division_team
    ADD CONSTRAINT season_division_team_season_division_id_fkey FOREIGN KEY (season_division_id) REFERENCES league_manager.season_division(id);


--
-- TOC entry 3210 (class 2606 OID 20987)
-- Name: season_division_team season_division_team_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_division_team
    ADD CONSTRAINT season_division_team_team_id_fkey FOREIGN KEY (team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3200 (class 2606 OID 20902)
-- Name: season season_league_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season
    ADD CONSTRAINT season_league_id_fkey FOREIGN KEY (league_id) REFERENCES league_manager.league(id);


--
-- TOC entry 3201 (class 2606 OID 20907)
-- Name: season season_match_type_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season
    ADD CONSTRAINT season_match_type_id_fkey FOREIGN KEY (match_type_id) REFERENCES league_manager.matchtype(id);


--
-- TOC entry 3229 (class 2606 OID 21138)
-- Name: season_registration season_registration_division_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_registration
    ADD CONSTRAINT season_registration_division_id_fkey FOREIGN KEY (division_id) REFERENCES league_manager.division(id);


--
-- TOC entry 3230 (class 2606 OID 21143)
-- Name: season_registration season_registration_player_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_registration
    ADD CONSTRAINT season_registration_player_id_fkey FOREIGN KEY (player_id) REFERENCES league_manager.player(id);


--
-- TOC entry 3231 (class 2606 OID 21148)
-- Name: season_registration season_registration_season_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_registration
    ADD CONSTRAINT season_registration_season_id_fkey FOREIGN KEY (season_id) REFERENCES league_manager.season(id);


--
-- TOC entry 3232 (class 2606 OID 21153)
-- Name: season_registration season_registration_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.season_registration
    ADD CONSTRAINT season_registration_team_id_fkey FOREIGN KEY (team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3211 (class 2606 OID 21000)
-- Name: team_award team_award_award_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team_award
    ADD CONSTRAINT team_award_award_id_fkey FOREIGN KEY (award_id) REFERENCES league_manager.award(id);


--
-- TOC entry 3212 (class 2606 OID 21005)
-- Name: team_award team_award_season_division_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team_award
    ADD CONSTRAINT team_award_season_division_id_fkey FOREIGN KEY (season_division_id) REFERENCES league_manager.season_division(id);


--
-- TOC entry 3213 (class 2606 OID 21010)
-- Name: team_award team_award_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team_award
    ADD CONSTRAINT team_award_team_id_fkey FOREIGN KEY (team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3233 (class 2606 OID 21166)
-- Name: team_invites team_invites_invited_player_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team_invites
    ADD CONSTRAINT team_invites_invited_player_id_fkey FOREIGN KEY (invited_player_id) REFERENCES league_manager.player(id);


--
-- TOC entry 3234 (class 2606 OID 21171)
-- Name: team_invites team_invites_inviting_player_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team_invites
    ADD CONSTRAINT team_invites_inviting_player_id_fkey FOREIGN KEY (inviting_player_id) REFERENCES league_manager.player(id);


--
-- TOC entry 3235 (class 2606 OID 21176)
-- Name: team_invites team_invites_team_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.team_invites
    ADD CONSTRAINT team_invites_team_id_fkey FOREIGN KEY (team_id) REFERENCES league_manager.team(id);


--
-- TOC entry 3196 (class 2606 OID 20857)
-- Name: twitch twitch_user_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.twitch
    ADD CONSTRAINT twitch_user_id_fkey FOREIGN KEY (user_id) REFERENCES league_manager."user"(id);


--
-- TOC entry 3197 (class 2606 OID 20871)
-- Name: user_permissions user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.user_permissions
    ADD CONSTRAINT user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES league_manager.permission(id);


--
-- TOC entry 3198 (class 2606 OID 20876)
-- Name: user_permissions user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: league_manager; Owner: postgres
--

ALTER TABLE ONLY league_manager.user_permissions
    ADD CONSTRAINT user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES league_manager."user"(id);




