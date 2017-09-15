--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: manufacturors; Type: TABLE; Schema: public; Owner: runarkristoffersen
--

CREATE TABLE manufacturors (
    id integer NOT NULL,
    name character varying(50),
    description character varying(500)
);


ALTER TABLE manufacturors OWNER TO runarkristoffersen;

--
-- Name: manufacturors_id_seq; Type: SEQUENCE; Schema: public; Owner: runarkristoffersen
--

CREATE SEQUENCE manufacturors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE manufacturors_id_seq OWNER TO runarkristoffersen;

--
-- Name: manufacturors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: runarkristoffersen
--

ALTER SEQUENCE manufacturors_id_seq OWNED BY manufacturors.id;


--
-- Name: product_specs; Type: TABLE; Schema: public; Owner: runarkristoffersen
--

CREATE TABLE product_specs (
    id integer NOT NULL,
    key character varying(25),
    value character varying(50),
    product_id integer
);


ALTER TABLE product_specs OWNER TO runarkristoffersen;

--
-- Name: product_specs_id_seq; Type: SEQUENCE; Schema: public; Owner: runarkristoffersen
--

CREATE SEQUENCE product_specs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE product_specs_id_seq OWNER TO runarkristoffersen;

--
-- Name: product_specs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: runarkristoffersen
--

ALTER SEQUENCE product_specs_id_seq OWNED BY product_specs.id;


--
-- Name: product_types; Type: TABLE; Schema: public; Owner: runarkristoffersen
--

CREATE TABLE product_types (
    id integer NOT NULL,
    name character varying(50),
    description character varying(500),
    "mainSpec" character varying(25),
    watt_per_meter numeric(6,0),
    watt_per_square_meter numeric(6,0),
    ledere integer,
    manufacturor_id integer
);


ALTER TABLE product_types OWNER TO runarkristoffersen;

--
-- Name: product_types_id_seq; Type: SEQUENCE; Schema: public; Owner: runarkristoffersen
--

CREATE SEQUENCE product_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE product_types_id_seq OWNER TO runarkristoffersen;

--
-- Name: product_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: runarkristoffersen
--

ALTER SEQUENCE product_types_id_seq OWNED BY product_types.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: runarkristoffersen
--

CREATE TABLE products (
    id integer NOT NULL,
    name character varying(50),
    effekt numeric(8,0),
    product_type_id integer
);


ALTER TABLE products OWNER TO runarkristoffersen;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: runarkristoffersen
--

CREATE SEQUENCE products_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE products_id_seq OWNER TO runarkristoffersen;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: runarkristoffersen
--

ALTER SEQUENCE products_id_seq OWNED BY products.id;


--
-- Name: manufacturors id; Type: DEFAULT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY manufacturors ALTER COLUMN id SET DEFAULT nextval('manufacturors_id_seq'::regclass);


--
-- Name: product_specs id; Type: DEFAULT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY product_specs ALTER COLUMN id SET DEFAULT nextval('product_specs_id_seq'::regclass);


--
-- Name: product_types id; Type: DEFAULT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY product_types ALTER COLUMN id SET DEFAULT nextval('product_types_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY products ALTER COLUMN id SET DEFAULT nextval('products_id_seq'::regclass);


--
-- Data for Name: manufacturors; Type: TABLE DATA; Schema: public; Owner: runarkristoffersen
--

COPY manufacturors (id, name, description) FROM stdin;
1	Nexans	It's nexans
2	Øglænd	It's øglænd
\.


--
-- Name: manufacturors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: runarkristoffersen
--

SELECT pg_catalog.setval('manufacturors_id_seq', 2, true);


--
-- Data for Name: product_specs; Type: TABLE DATA; Schema: public; Owner: runarkristoffersen
--

COPY product_specs (id, key, value, product_id) FROM stdin;
1	Elnr	10 372 00	1
2	Lengde	7	1
3	Resistans_min	457	1
4	Resistans_max	529	1
5	Driftstrøm	0,5	1
6	Vekt	0,7	1
7	Elnr	10 372 01	2
8	Lengde	10	2
9	Resistans_min	314	2
10	Resistans_max	364	2
11	Driftstrøm	0,7	2
12	Vekt	0,8	2
13	Elnr	10 372 02	3
14	Lengde	14	3
15	Resistans_min	228	3
16	Resistans_max	265	3
17	Driftstrøm	1,0	3
18	Vekt	1,0	3
19	Elnr	10 372 03	4
20	Lengde	19	4
21	Resistans_min	168	4
22	Resistans_max	194	4
23	Driftstrøm	1,3	4
24	Vekt	1,2	4
25	Elnr	10 372 04	5
26	Lengde	24	5
27	Resistans_min	126	5
28	Resistans_max	145	5
29	Driftstrøm	1,7	5
30	Vekt	1,4	5
31	Elnr	10 372 05	6
32	Lengde	31	6
33	Resistans_min	101	6
34	Resistans_max	116	6
35	Driftstrøm	2,2	6
36	Vekt	1,7	6
37	Elnr	10 363 60	7
38	Lengde	38	7
39	Resistans_min	83	7
40	Resistans_max	97	7
41	Driftstrøm	2,6	7
42	Vekt	2,0	7
43	Elnr	10 363 61	8
44	Lengde	44	8
45	Resistans_min	72	8
46	Resistans_max	84	8
47	Driftstrøm	3,0	8
48	Vekt	2,2	8
49	Elnr	10 372 07	9
50	Lengde	50	9
51	Resistans_min	63	9
52	Resistans_max	73	9
53	Driftstrøm	3,5	9
54	Vekt	2,5	9
55	Elnr	10 372 08	10
56	Lengde	55	10
57	Resistans_min	56	10
58	Resistans_max	65	10
59	Driftstrøm	3,9	10
60	Vekt	2,7	10
61	Elnr	10 372 32	11
62	Lengde	64	11
63	Resistans_min	50	11
64	Resistans_max	59	11
65	Driftstrøm	4,3	11
66	Vekt	3,1	11
67	Elnr	10 372 09	12
68	Lengde	72	12
69	Resistans_min	44	12
70	Resistans_max	51	12
71	Driftstrøm	5,0	12
72	Vekt	3,5	12
73	Elnr	10 372 13	13
74	Lengde	82	13
75	Resistans_min	39	13
76	Resistans_max	45	13
77	Driftstrøm	5,7	13
78	Vekt	3,9	13
79	Elnr	10 372 10	14
80	Lengde	92	14
81	Resistans_min	34	14
82	Resistans_max	39	14
83	Driftstrøm	6,5	14
84	Vekt	4,3	14
85	Elnr	10 372 11	15
86	Lengde	112	15
87	Resistans_min	28	15
88	Resistans_max	33	15
89	Driftstrøm	7,8	15
90	Vekt	5,2	15
91	Elnr	10 372 14	16
92	Lengde	126	16
93	Resistans_min	25	16
94	Resistans_max	29	16
95	Driftstrøm	8,7	16
96	Vekt	5,8	16
97	Elnr	10 372 12	17
98	Lengde	144	17
99	Resistans_min	22	17
100	Resistans_max	25	17
101	Driftstrøm	10,0	17
102	Vekt	6,5	17
103	Elnr	10 363 62	18
104	Lengde	155	18
105	Resistans_min	20	18
106	Resistans_max	23	18
107	Driftstrøm	11,1	18
108	Vekt	7,0	18
109	Elnr	10 363 63	19
110	Lengde	175	19
111	Resistans_min	18	19
112	Resistans_max	21	19
113	Driftstrøm	12,2	19
114	Vekt	7,8	19
115	Elnr	10 363 64	20
116	Lengde	188	20
117	Resistans_min	17	20
118	Resistans_max	20	20
119	Driftstrøm	13,0	20
120	Vekt	8,4	20
121	Elnr	10 372 15	21
122	Lengde	6	21
123	Resistans_min	1142	21
124	Resistans_max	1323	21
125	Driftstrøm	0,2	21
126	Vekt	0,6	21
127	Elnr	10 372 16	22
128	Lengde	8	22
129	Resistans_min	838	22
130	Resistans_max	970	22
131	Driftstrøm	0,3	22
132	Vekt	0,7	22
133	Elnr	10 372 17	23
134	Lengde	10	23
135	Resistans_min	670	23
136	Resistans_max	776	23
137	Driftstrøm	0,4	23
138	Vekt	0,8	23
139	Elnr	10 372 18	24
140	Lengde	15	24
141	Resistans_min	457	24
142	Resistans_max	529	24
143	Driftstrøm	0,5	24
144	Vekt	1,0	24
145	Elnr	10 372 19	25
146	Lengde	20	25
147	Resistans_min	335	25
148	Resistans_max	388	25
149	Driftstrøm	0,7	25
150	Vekt	1,2	25
151	Elnr	10 372 20	26
152	Lengde	25	26
153	Resistans_min	265	26
154	Resistans_max	306	26
155	Driftstrøm	0,8	26
156	Vekt	1,4	26
157	Elnr	10 372 21	27
158	Lengde	30	27
159	Resistans_min	223	27
160	Resistans_max	259	27
161	Driftstrøm	1,0	27
162	Vekt	1,6	27
163	Elnr	10 372 22	28
164	Lengde	35	28
165	Resistans_min	193	28
166	Resistans_max	224	28
167	Driftstrøm	1,1	28
168	Vekt	1,9	28
169	Elnr	10 372 23	29
170	Lengde	40	29
171	Resistans_min	168	29
172	Resistans_max	194	29
173	Driftstrøm	1,3	29
174	Vekt	2,1	29
175	Elnr	10 372 24	30
176	Lengde	45	30
177	Resistans_min	148	30
178	Resistans_max	171	30
179	Driftstrøm	1,5	30
180	Vekt	2,3	30
181	Elnr	10 372 25	31
182	Lengde	50	31
183	Resistans_min	134	31
184	Resistans_max	155	31
185	Driftstrøm	1,6	31
186	Vekt	2,5	31
187	Elnr	10 372 26	32
188	Lengde	60	32
189	Resistans_min	112	32
190	Resistans_max	129	32
191	Driftstrøm	2,0	32
192	Vekt	3,0	32
193	Elnr	10 363 65	33
194	Lengde	70	33
195	Resistans_min	95	33
196	Resistans_max	111	33
197	Driftstrøm	2,3	33
198	Vekt	3,4	33
199	Elnr	10 372 27	34
200	Lengde	80	34
201	Resistans_min	84	34
202	Resistans_max	97	34
203	Driftstrøm	2,6	34
204	Vekt	3,9	34
205	Elnr	10 363 66	35
206	Lengde	90	35
207	Resistans_min	74	35
208	Resistans_max	87	35
209	Driftstrøm	2,9	35
210	Vekt	4,3	35
211	Elnr	10 372 28	36
212	Lengde	105	36
213	Resistans_min	64	36
214	Resistans_max	74	36
215	Driftstrøm	3,4	36
216	Vekt	4,9	36
217	Elnr	10 363 67	37
218	Lengde	120	37
219	Resistans_min	56	37
220	Resistans_max	65	37
221	Driftstrøm	3,9	37
222	Vekt	5,5	37
223	Elnr	10 372 29	38
224	Lengde	135	38
225	Resistans_min	50	38
226	Resistans_max	58	38
227	Driftstrøm	4,4	38
228	Vekt	6,2	38
229	Elnr	10 363 68	39
230	Lengde	155	39
231	Resistans_min	44	39
232	Resistans_max	50	39
233	Driftstrøm	5,1	39
234	Vekt	7,0	39
235	Elnr	10 363 69	40
236	Lengde	185	40
237	Resistans_min	37	40
238	Resistans_max	42	40
239	Driftstrøm	6,0	40
240	Vekt	8,3	40
241	Elnr	10 367 32	41
242	Lengde	13	41
243	Resistans_min	387	41
244	Resistans_max	448	41
245	Driftstrøm	0,6	41
246	Vekt	1,0	41
247	Elnr	10 367 33	42
248	Lengde	22	42
249	Resistans_min	228	42
250	Resistans_max	265	42
251	Driftstrøm	1,0	42
252	Vekt	1,3	42
253	Elnr	10 367 34	43
254	Lengde	30	43
255	Resistans_min	168	43
256	Resistans_max	194	43
257	Driftstrøm	1,3	43
258	Vekt	1,7	43
259	Elnr	10 367 35	44
260	Lengde	43	44
261	Resistans_min	117	44
262	Resistans_max	135	44
263	Driftstrøm	1,9	44
264	Vekt	2,2	44
265	Elnr	10 367 36	45
266	Lengde	52	45
267	Resistans_min	97	45
268	Resistans_max	112	45
269	Driftstrøm	2,3	45
270	Vekt	2,6	45
271	Elnr	10 367 37	46
272	Lengde	63	46
273	Resistans_min	80	46
274	Resistans_max	93	46
275	Driftstrøm	2,7	46
276	Vekt	3,1	46
277	Elnr	10 367 38	47
278	Lengde	70	47
279	Resistans_min	72	47
280	Resistans_max	83	47
281	Driftstrøm	3,0	47
282	Vekt	3,4	47
283	Elnr	10 367 39	48
284	Lengde	80	48
285	Resistans_min	63	48
286	Resistans_max	73	48
287	Driftstrøm	3,5	48
288	Vekt	3,8	48
289	Elnr	10 367 42	49
290	Lengde	91	49
291	Resistans_min	55	49
292	Resistans_max	64	49
293	Driftstrøm	4,0	49
294	Vekt	4,3	49
295	Elnr	10 367 43	50
296	Lengde	100	50
297	Resistans_min	50	50
298	Resistans_max	58	50
299	Driftstrøm	4,3	50
300	Vekt	4,7	50
301	Elnr	10 367 44	51
302	Lengde	117	51
303	Resistans_min	43	51
304	Resistans_max	50	51
305	Driftstrøm	5,1	51
306	Vekt	5,4	51
307	Elnr	10 367 55	52
308	Lengde	130	52
309	Resistans_min	39	52
310	Resistans_max	45	52
311	Driftstrøm	5,7	52
312	Vekt	6,0	52
313	Elnr	10 367 45	53
314	Lengde	142	53
315	Resistans_min	35	53
316	Resistans_max	41	53
317	Driftstrøm	6,2	53
318	Vekt	6,5	53
319	Elnr	10 367 56	54
320	Lengde	160	54
321	Resistans_min	31	54
322	Resistans_max	37	54
323	Driftstrøm	7,0	54
324	Vekt	7,2	54
325	Elnr	10 367 46	55
326	Lengde	182	55
327	Resistans_min	28	55
328	Resistans_max	32	55
329	Driftstrøm	7,9	55
330	Vekt	8,1	55
331	Elnr	10 630 00	56
332	Lengde	35	56
333	Resistans_min	47	56
334	Resistans_max	56	56
335	Driftstrøm	4,6	56
336	Vekt	2,9	56
337	\N	{""}	56
338	Elnr	10 630 01	57
339	Lengde	50	57
340	Resistans_min	33	57
341	Resistans_max	39	57
342	Driftstrøm	6,5	57
343	Vekt	3,7	57
344	\N	{""}	57
345	Elnr	10 630 02	58
346	Lengde	60	58
347	Resistans_min	27	58
348	Resistans_max	33	58
349	Driftstrøm	7,8	58
350	Vekt	4,1	58
351	\N	{""}	58
352	Elnr	10 630 03	59
353	Lengde	70	59
354	Resistans_min	23	59
355	Resistans_max	28	59
356	Driftstrøm	9,1	59
357	Vekt	5,2	59
358	\N	{""}	59
359	Elnr	10 630 04	60
360	Lengde	80	60
361	Resistans_min	20	60
362	Resistans_max	25	60
363	Driftstrøm	10,4	60
364	Vekt	5,7	60
365	\N	{""}	60
366	Elnr	10 630 05	61
367	Lengde	90	61
368	Resistans_min	18	61
369	Resistans_max	22	61
370	Driftstrøm	11,7	61
371	Vekt	6,0	61
372	\N	{""}	61
373	Elnr	10 630 06	62
374	Lengde	100	62
375	Resistans_min	16	62
376	Resistans_max	20	62
377	Driftstrøm	13,0	62
378	Vekt	6,5	62
379	\N	{""}	62
380	Elnr	10 630 07	63
381	Lengde	120	63
382	Resistans_min	14	63
383	Resistans_max	17	63
384	Driftstrøm	15,7	63
385	Vekt	7,5	63
386	\N	{""}	63
387	Elnr	10 630 08	64
388	Lengde	150	64
389	Resistans_min	11	64
390	Resistans_max	13	64
391	Driftstrøm	19,6	64
392	Vekt	10,7	64
393	\N	{""}	64
394	Elnr	10 630 09	65
395	Lengde	170	65
396	Resistans_min	9	65
397	Resistans_max	12	65
398	Driftstrøm	22,2	65
399	Vekt	12,0	65
400	\N	{""}	65
401	Elnr	10 630 10	66
402	Lengde	200	66
403	Resistans_min	8	66
404	Resistans_max	10	66
405	Driftstrøm	26,1	66
406	Vekt	13,8	66
407	\N	{""}	66
408	Elnr	10 374 20	67
409	Lengde	90	67
410	Resistans_min	56	67
411	Resistans_max	65	67
412	Driftstrøm	6,8	67
413	Vekt	10,6	67
414	Elnr	10 374 21	68
415	Lengde	100	68
416	Resistans_min	51	68
417	Resistans_max	59	68
418	Driftstrøm	7,5	68
419	Vekt	11,6	68
420	Elnr	10 374 22	69
421	Lengde	120	69
422	Resistans_min	42	69
423	Resistans_max	49	69
424	Driftstrøm	9,0	69
425	Vekt	13,6	69
426	Elnr	10 374 23	70
427	Lengde	150	70
428	Resistans_min	34	70
429	Resistans_max	39	70
430	Driftstrøm	11,3	70
431	Vekt	17,6	70
432	Elnr	10 374 24	71
433	Lengde	170	71
434	Resistans_min	30	71
435	Resistans_max	35	71
436	Driftstrøm	12,8	71
437	Vekt	19,6	71
438	Elnr	10 374 25	72
439	Lengde	200	72
440	Resistans_min	25	72
441	Resistans_max	29	72
442	Driftstrøm	15,0	72
443	Vekt	22,6	72
444	Elnr	10 374 60	73
445	Bredde	0,5	73
446	Lengde	18	73
447	Areal	9	73
448	Resistans_min	56	73
449	Resistans_max	65	73
450	Driftstrøm	6,8	73
451	Vekt	11,7	73
452	Elnr	10 374 61	74
453	Bredde	0,5	74
454	Lengde	20	74
455	Areal	10	74
456	Resistans_min	51	74
457	Resistans_max	59	74
458	Driftstrøm	7,5	74
459	Vekt	12,8	74
460	Elnr	10 374 62	75
461	Bredde	0,5	75
462	Lengde	24	75
463	Areal	12	75
464	Resistans_min	42	75
465	Resistans_max	49	75
466	Driftstrøm	9,0	75
467	Vekt	14,9	75
468	Elnr	10 374 70	76
469	Bredde	1,0	76
470	Lengde	10	76
471	Areal	10	76
472	Resistans_min	51	76
473	Resistans_max	59	76
474	Driftstrøm	7,5	76
475	Vekt	12,9	76
476	Elnr	10 374 71	77
477	Bredde	1,0	77
478	Lengde	12	77
479	Areal	12	77
480	Resistans_min	42	77
481	Resistans_max	49	77
482	Driftstrøm	9,0	77
483	Vekt	15,1	77
484	Elnr	10 374 72	78
485	Bredde	1,0	78
486	Lengde	15	78
487	Areal	15	78
488	Resistans_min	34	78
489	Resistans_max	39	78
490	Driftstrøm	11,3	78
491	Vekt	18,7	78
492	Elnr	10 374 73	79
493	Bredde	1,0	79
494	Lengde	17	79
495	Areal	17	79
496	Resistans_min	30	79
497	Resistans_max	35	79
498	Driftstrøm	12,8	79
499	Vekt	20,9	79
500	Elnr	10 374 74	80
501	Bredde	1,0	80
502	Lengde	20	80
503	Areal	20	80
504	Resistans_min	25	80
505	Resistans_max	29	80
506	Driftstrøm	15,0	80
507	Vekt	24,2	80
508	Elnr	10 374 30	81
509	Bredde	0,5	81
510	Lengde	7	81
511	Areal	3,5	81
512	Resistans_min	47	81
513	Resistans_max	56	81
514	Driftstrøm	4,6	81
515	Vekt	5,5	81
516	Elnr	10 374 31	82
517	Bredde	0,5	82
518	Lengde	10	82
519	Areal	5	82
520	Resistans_min	33	82
521	Resistans_max	39	82
522	Driftstrøm	6,5	82
523	Vekt	7,1	82
524	Elnr	10 374 32	83
525	Bredde	0,5	83
526	Lengde	12	83
527	Areal	6	83
528	Resistans_min	27	83
529	Resistans_max	33	83
530	Driftstrøm	7,8	83
531	Vekt	8,2	83
532	Elnr	10 374 33	84
533	Bredde	0,5	84
534	Lengde	14	84
535	Areal	7	84
536	Resistans_min	23	84
537	Resistans_max	28	84
538	Driftstrøm	9,1	84
539	Vekt	9,3	84
540	Elnr	10 374 34	85
541	Bredde	0,5	85
542	Lengde	16	85
543	Areal	8	85
544	Resistans_min	20	85
545	Resistans_max	25	85
546	Driftstrøm	10,4	85
547	Vekt	10,6	85
548	Elnr	10 374 35	86
549	Bredde	0,5	86
550	Lengde	18	86
551	Areal	9	86
552	Resistans_min	18	86
553	Resistans_max	22	86
554	Driftstrøm	11,7	86
555	Vekt	11,7	86
556	Elnr	10 374 36	87
557	Bredde	0,5	87
558	Lengde	20	87
559	Areal	10	87
560	Resistans_min	16	87
561	Resistans_max	20	87
562	Driftstrøm	13,0	87
563	Vekt	12,8	87
564	Elnr	10 374 37	88
565	Bredde	0,5	88
566	Lengde	24	88
567	Areal	12	88
568	Resistans_min	14	88
569	Resistans_max	17	88
570	Driftstrøm	15,7	88
571	Vekt	15,0	88
572	Elnr	10 374 45	89
573	Bredde	1,0	89
574	Lengde	10	89
575	Areal	10	89
576	Resistans_min	16	89
577	Resistans_max	20	89
578	Driftstrøm	13,0	89
579	Vekt	12,9	89
580	Elnr	10 374 46	90
581	Bredde	1,0	90
582	Lengde	12	90
583	Areal	12	90
584	Resistans_min	14	90
585	Resistans_max	17	90
586	Driftstrøm	15,7	90
587	Vekt	15,1	90
588	Elnr	10 374 47	91
589	Bredde	1,0	91
590	Lengde	15	91
591	Areal	15	91
592	Resistans_min	11	91
593	Resistans_max	13	91
594	Driftstrøm	19,6	91
595	Vekt	19,5	91
596	Elnr	10 374 48	92
597	Bredde	1,0	92
598	Lengde	17	92
599	Areal	17	92
600	Resistans_min	9	92
601	Resistans_max	12	92
602	Driftstrøm	22,2	92
603	Vekt	22,1	92
604	Elnr	10 374 49	93
605	Bredde	1,0	93
606	Lengde	20	93
607	Areal	20	93
608	Resistans_min	8	93
609	Resistans_max	10	93
610	Driftstrøm	26,1	93
611	Vekt	25,4	93
612	Elnr	10 363 40	94
613	Bredde	0,5	94
614	Lengde	1	94
615	Areal	0,5	94
616	Resistans_min	838	94
617	Resistans_max	970	94
618	Driftstrøm	0,3	94
619	Vekt	0,7	94
620	Elnr	10 363 41	95
621	Bredde	0,5	95
622	Lengde	2	95
623	Areal	1,0	95
624	Resistans_min	419	95
625	Resistans_max	485	95
626	Driftstrøm	0,5	95
627	Vekt	0,8	95
628	Elnr	10 363 42	96
629	Bredde	0,5	96
630	Lengde	3	96
631	Areal	1,5	96
632	Resistans_min	279	96
633	Resistans_max	323	96
634	Driftstrøm	0,8	96
635	Vekt	1,0	96
636	Elnr	10 363 43	97
637	Bredde	0,5	97
638	Lengde	4	97
639	Areal	2,0	97
640	Resistans_min	209	97
641	Resistans_max	242	97
642	Driftstrøm	1,0	97
643	Vekt	1,1	97
644	Elnr	10 363 44	98
645	Bredde	0,5	98
646	Lengde	5	98
647	Areal	2,5	98
648	Resistans_min	167	98
649	Resistans_max	194	98
650	Driftstrøm	1,3	98
651	Vekt	1,2	98
652	Elnr	10 363 45	99
653	Bredde	0,5	99
654	Lengde	6	99
655	Areal	3,0	99
656	Resistans_min	140	99
657	Resistans_max	162	99
658	Driftstrøm	1,6	99
659	Vekt	1,4	99
660	Elnr	10 363 46	100
661	Bredde	0,5	100
662	Lengde	7	100
663	Areal	3,5	100
664	Resistans_min	120	100
665	Resistans_max	139	100
666	Driftstrøm	1,9	100
667	Vekt	1,5	100
668	Elnr	10 363 47	101
669	Bredde	0,5	101
670	Lengde	8	101
671	Areal	4,0	101
672	Resistans_min	105	101
673	Resistans_max	121	101
674	Driftstrøm	2,1	101
675	Vekt	1,6	101
676	Elnr	10 363 48	102
677	Bredde	0,5	102
678	Lengde	10	102
679	Areal	5,0	102
680	Resistans_min	84	102
681	Resistans_max	97	102
682	Driftstrøm	2,6	102
683	Vekt	1,9	102
684	Elnr	10 363 49	103
685	Bredde	0,5	103
686	Lengde	12	103
687	Areal	6,0	103
688	Resistans_min	69	103
689	Resistans_max	80	103
690	Driftstrøm	3,2	103
691	Vekt	2,3	103
692	Elnr	10 363 50	104
693	Bredde	0,5	104
694	Lengde	14	104
695	Areal	7,0	104
696	Resistans_min	60	104
697	Resistans_max	69	104
698	Driftstrøm	3,7	104
699	Vekt	2,6	104
700	Elnr	10 363 51	105
701	Bredde	0,5	105
702	Lengde	16	105
703	Areal	8,0	105
704	Resistans_min	52	105
705	Resistans_max	61	105
706	Driftstrøm	4,2	105
707	Vekt	2,8	105
708	Elnr	10 363 52	106
709	Bredde	0,5	106
710	Lengde	18	106
711	Areal	9,0	106
712	Resistans_min	47	106
713	Resistans_max	54	106
714	Driftstrøm	4,7	106
715	Vekt	3,1	106
716	Elnr	10 363 53	107
717	Bredde	0,5	107
718	Lengde	20	107
719	Areal	10,0	107
720	Resistans_min	42	107
721	Resistans_max	49	107
722	Driftstrøm	5,2	107
723	Vekt	3,4	107
724	Elnr	10 363 54	108
725	Bredde	0,5	108
726	Lengde	22	108
727	Areal	11,0	108
728	Resistans_min	38	108
729	Resistans_max	44	108
730	Driftstrøm	5,8	108
731	Vekt	3,6	108
732	Elnr	10 363 55	109
733	Bredde	0,5	109
734	Lengde	24	109
735	Areal	12,0	109
736	Resistans_min	35	109
737	Resistans_max	40	109
738	Driftstrøm	6,3	109
739	Vekt	3,9	109
740	Elnr	10 363 20	110
741	Bredde	0,5	110
742	Lengde	1	110
743	Areal	0,5	110
744	Resistans_min	1256	110
745	Resistans_max	1455	110
746	Driftstrøm	0,2	110
747	Vekt	0,7	110
748	Elnr	10 363 21	111
749	Bredde	0,5	111
750	Lengde	2	111
751	Areal	1,0	111
752	Resistans_min	628	111
753	Resistans_max	727	111
754	Driftstrøm	0,4	111
755	Vekt	0,8	111
756	Elnr	10 363 22	112
757	Bredde	0,5	112
758	Lengde	3	112
759	Areal	1,5	112
760	Resistans_min	419	112
761	Resistans_max	485	112
762	Driftstrøm	0,5	112
763	Vekt	1,0	112
764	Elnr	10 363 23	113
765	Bredde	0,5	113
766	Lengde	4	113
767	Areal	2,0	113
768	Resistans_min	314	113
769	Resistans_max	364	113
770	Driftstrøm	0,7	113
771	Vekt	1,1	113
772	Elnr	10 363 24	114
773	Bredde	0,5	114
774	Lengde	5	114
775	Areal	2,5	114
776	Resistans_min	252	114
777	Resistans_max	292	114
778	Driftstrøm	0,9	114
779	Vekt	1,2	114
780	Elnr	10 363 25	115
781	Bredde	0,5	115
782	Lengde	6	115
783	Areal	3,0	115
784	Resistans_min	209	115
785	Resistans_max	242	115
786	Driftstrøm	1,0	115
787	Vekt	1,4	115
788	Elnr	10 363 26	116
789	Bredde	0,5	116
790	Lengde	7	116
791	Areal	3,5	116
792	Resistans_min	179	116
793	Resistans_max	208	116
794	Driftstrøm	1,2	116
795	Vekt	1,5	116
796	Elnr	10 363 27	117
797	Bredde	0,5	117
798	Lengde	8	117
799	Areal	4,0	117
800	Resistans_min	157	117
801	Resistans_max	182	117
802	Driftstrøm	1,4	117
803	Vekt	1,6	117
804	Elnr	10 363 28	118
805	Bredde	0,5	118
806	Lengde	10	118
807	Areal	5,0	118
808	Resistans_min	125	118
809	Resistans_max	145	118
810	Driftstrøm	1,8	118
811	Vekt	1,9	118
812	Elnr	10 363 29	119
813	Bredde	0,5	119
814	Lengde	12	119
815	Areal	6,0	119
816	Resistans_min	104	119
817	Resistans_max	121	119
818	Driftstrøm	2,1	119
819	Vekt	2,3	119
820	Elnr	10 363 30	120
821	Bredde	0,5	120
822	Lengde	14	120
823	Areal	7,0	120
824	Resistans_min	90	120
825	Resistans_max	104	120
826	Driftstrøm	2,5	120
827	Vekt	2,6	120
828	Elnr	10 363 31	121
829	Bredde	0,5	121
830	Lengde	16	121
831	Areal	8,0	121
832	Resistans_min	78	121
833	Resistans_max	91	121
834	Driftstrøm	2,8	121
835	Vekt	2,8	121
836	Elnr	10 363 32	122
837	Bredde	0,5	122
838	Lengde	18	122
839	Areal	9,0	122
840	Resistans_min	70	122
841	Resistans_max	81	122
842	Driftstrøm	3,2	122
843	Vekt	3,1	122
844	Elnr	10 363 33	123
845	Bredde	0,5	123
846	Lengde	20	123
847	Areal	10,0	123
848	Resistans_min	62	123
849	Resistans_max	73	123
850	Driftstrøm	3,5	123
851	Vekt	3,4	123
852	Elnr	10 363 34	124
853	Bredde	0,5	124
854	Lengde	22	124
855	Areal	11,0	124
856	Resistans_min	57	124
857	Resistans_max	66	124
858	Driftstrøm	3,9	124
859	Vekt	3,6	124
860	Elnr	10 363 35	125
861	Bredde	0,5	125
862	Lengde	24	125
863	Areal	12,0	125
864	Resistans_min	52	125
865	Resistans_max	61	125
866	Driftstrøm	4,2	125
867	Vekt	3,9	125
868	Lengde	23	126
869	Nominell elementmotstand	230,0	126
870	Ytre dimensjoner	7,0	126
871	Vekt	1,7	126
872	Elnr	10 365 14	126
873	Nexans art. nr.	10224179	126
874	GTIN	7045210068856	126
875	Lengde	38,3	127
876	Nominell elementmotstand	139,2	127
877	Ytre dimensjoner	7,0	127
878	Vekt	2,7	127
879	Elnr	10 365 15	127
880	Nexans art. nr.	10224180	127
881	GTIN	7045210068863	127
882	Lengde	53,4	128
883	Nominell elementmotstand	99,8	128
884	Ytre dimensjoner	7,0	128
885	Vekt	3,7	128
886	Elnr	10 365 16	128
887	Nexans art. nr.	10224181	128
888	GTIN	7045210068870	128
889	Lengde	64,8	129
890	Nominell elementmotstand	81,4	129
891	Ytre dimensjoner	7,0	129
892	Vekt	4,2	129
893	Elnr	10 365 33	129
894	Nexans art. nr.	10224182	129
895	GTIN	7045210068887	129
896	Lengde	76,0	130
897	Nominell elementmotstand	69,6	130
898	Ytre dimensjoner	7,0	130
899	Vekt	5,2	130
900	Elnr	10 365 17	130
901	Nexans art. nr.	10224183	130
902	GTIN	7045210068894	130
903	Lengde	94,4	131
904	Nominell elementmotstand	56,3	131
905	Ytre dimensjoner	7,0	131
906	Vekt	6,4	131
907	Elnr	10 365 18	131
908	Nexans art. nr.	10224224	131
909	GTIN	7045210068900	131
910	Lengde	105,4	132
911	Nominell elementmotstand	50,4	132
912	Ytre dimensjoner	7,0	132
913	Vekt	6,9	132
914	Elnr	10 365 19	132
915	Nexans art. nr.	10224225	132
916	GTIN	7045210068917	132
917	Lengde	130,4	133
918	Nominell elementmotstand	40,7	133
919	Ytre dimensjoner	7,0	133
920	Vekt	8,6	133
921	Elnr	10 365 20	133
922	Nexans art. nr.	10224226	133
923	GTIN	7045210068924	133
924	Lengde	161,3	134
925	Nominell elementmotstand	32,9	134
926	Ytre dimensjoner	7,0	134
927	Vekt	10,7	134
928	Elnr	10 365 21	134
929	Nexans art. nr.	10224227	134
930	GTIN	7045210068931	134
931	Lengde	11,7	135
932	Nominell elementmotstand	264,5	135
933	Ytre dimensjoner	7,0	135
934	Vekt	1,2	135
935	Elnr	10 366 40	135
936	Nexans art. nr.	10224120	135
937	GTIN	7045210068511	135
938	Lengde	17,6	136
939	Nominell elementmotstand	176,3	136
940	Ytre dimensjoner	7,0	136
941	Vekt	1,4	136
942	Elnr	10 366 42	136
943	Nexans art. nr.	10224185	136
944	GTIN	7045210068528	136
945	Lengde	23,5	137
946	Nominell elementmotstand	132,3	137
947	Ytre dimensjoner	7,0	137
948	Vekt	1,8	137
949	Elnr	10 366 44	137
950	Nexans art. nr.	10224186	137
951	GTIN	7045210068535	137
952	Lengde	29,3	138
953	Nominell elementmotstand	105,8	138
954	Ytre dimensjoner	7,0	138
955	Vekt	2,2	138
956	Elnr	10 366 46	138
957	Nexans art. nr.	10224187	138
958	GTIN	7045210068542	138
959	Lengde	35,2	139
960	Nominell elementmotstand	88,2	139
961	Ytre dimensjoner	7,0	139
962	Vekt	2,6	139
963	Elnr	10 366 48	139
964	Nexans art. nr.	10224188	139
965	GTIN	7045210068559	139
966	Lengde	41,0	140
967	Nominell elementmotstand	75,6	140
968	Ytre dimensjoner	7,0	140
969	Vekt	2,9	140
970	Elnr	10 366 50	140
971	Nexans art. nr.	10224189	140
972	GTIN	7045210068566	140
973	Lengde	49,7	141
974	Nominell elementmotstand	63,0	141
975	Ytre dimensjoner	7,0	141
976	Vekt	3,5	141
977	Elnr	10 366 52	141
978	Nexans art. nr.	10224190	141
979	GTIN	7045210068573	141
980	Lengde	58,3	142
981	Nominell elementmotstand	52,9	142
982	Ytre dimensjoner	7,0	142
983	Vekt	4,1	142
984	Elnr	10 366 54	142
985	Nexans art. nr.	10224191	142
986	GTIN	7045210068580	142
987	Lengde	72,4	143
988	Nominell elementmotstand	42,3	143
989	Ytre dimensjoner	7,0	143
990	Vekt	5,0	143
991	Elnr	10 366 56	143
992	Nexans art. nr.	10224192	143
993	GTIN	7045210068597	143
994	Lengde	80,8	144
995	Nominell elementmotstand	38,6	144
996	Ytre dimensjoner	7,0	144
997	Vekt	5,3	144
998	Elnr	10 366 58	144
999	Nexans art. nr.	10224193	144
1000	GTIN	7045210068801	144
1001	Lengde	86,4	145
1002	Nominell elementmotstand	35,3	145
1003	Ytre dimensjoner	7,0	145
1004	Vekt	6,1	145
1005	Elnr	10 366 59	145
1006	Nexans art. nr.	10263199	145
1007	GTIN	7045210079562	145
1008	Lengde	100,0	146
1009	Nominell elementmotstand	31,1	146
1010	Ytre dimensjoner	7,0	146
1011	Vekt	6,7	146
1012	Elnr	10 366 60	146
1013	Nexans art. nr.	10224204	146
1014	GTIN	7045210068818	146
1015	Lengde	123,7	147
1016	Nominell elementmotstand	25,2	147
1017	Ytre dimensjoner	7,0	147
1018	Vekt	8,3	147
1019	Elnr	10 366 62	147
1020	Nexans art. nr.	10224205	147
1021	GTIN	7045210068825	147
1022	Lengde	154,5	148
1023	Nominell elementmotstand	20,3	148
1024	Ytre dimensjoner	7,0	148
1025	Vekt	10,1	148
1026	Elnr	10 366 64	148
1027	Nexans art. nr.	10224206	148
1028	GTIN	7045210068832	148
1029	Lengde	194,0	149
1030	Nominell elementmotstand	16,0	149
1031	Ytre dimensjoner	7,0	149
1032	Vekt	12,4	149
1033	Elnr	10 366 66	149
1034	Nexans art. nr.	10224207	149
1035	GTIN	7045210068849	149
\.


--
-- Name: product_specs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: runarkristoffersen
--

SELECT pg_catalog.setval('product_specs_id_seq', 1035, true);


--
-- Data for Name: product_types; Type: TABLE DATA; Schema: public; Owner: runarkristoffersen
--

COPY product_types (id, name, description, "mainSpec", watt_per_meter, watt_per_square_meter, ledere, manufacturor_id) FROM stdin;
1	ØS-30-21-16Wm	\N	TADA	16	\N	2	2
2	ØS-30-21L-8Wm	\N	TADA	8	\N	2	2
3	ØS-GG-10-10Wm	\N	TADA	10	\N	2	2
4	ØS-Snøkabel-Lett-30-30Wm-230V	\N	TADA	30	\N	2	2
5	ØS-Snøkabel-Lett-30-30Wm-400V	\N	TADA	30	\N	2	2
6	ØS-Snømatte-300Wkvm-400V	\N	TADA	\N	300	2	2
7	ØS-Snømatte-300Wkvm	\N	TADA	\N	300	2	2
8	ØS-Varmematte-120Wkvm	\N	TADA	\N	120	2	2
9	ØS-Varmematte-80Wkvm	\N	TADA	\N	80	2	2
10	TXLP-10Wm	\N	TADA	10	\N	2	1
11	TXLP-17Wm	\N	TADA	17	\N	2	1
\.


--
-- Name: product_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: runarkristoffersen
--

SELECT pg_catalog.setval('product_types_id_seq', 11, true);


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: runarkristoffersen
--

COPY products (id, name, effekt, product_type_id) FROM stdin;
1	ØS-30-21-16Wm-110	110	1
2	ØS-30-21-16Wm-160	160	1
3	ØS-30-21-16Wm-220	220	1
4	ØS-30-21-16Wm-300	300	1
5	ØS-30-21-16Wm-400	400	1
6	ØS-30-21-16Wm-500	500	1
7	ØS-30-21-16Wm-600	600	1
8	ØS-30-21-16Wm-700	700	1
9	ØS-30-21-16Wm-800	800	1
10	ØS-30-21-16Wm-900	900	1
11	ØS-30-21-16Wm-1000	1000	1
12	ØS-30-21-16Wm-1150	1150	1
13	ØS-30-21-16Wm-1300	1300	1
14	ØS-30-21-16Wm-1500	1500	1
15	ØS-30-21-16Wm-1800	1800	1
16	ØS-30-21-16Wm-2000	2000	1
17	ØS-30-21-16Wm-2300	2300	1
18	ØS-30-21-16Wm-2550	2550	1
19	ØS-30-21-16Wm-2800	2800	1
20	ØS-30-21-16Wm-3000	3000	1
21	ØS-30-21L-8Wm-44	44	2
22	ØS-30-21L-8Wm-60	60	2
23	ØS-30-21L-8Wm-75	75	2
24	ØS-30-21L-8Wm-110	110	2
25	ØS-30-21L-8Wm-150	150	2
26	ØS-30-21L-8Wm-190	190	2
27	ØS-30-21L-8Wm-225	225	2
28	ØS-30-21L-8Wm-260	260	2
29	ØS-30-21L-8Wm-300	300	2
30	ØS-30-21L-8Wm-340	340	2
31	ØS-30-21L-8Wm-375	375	2
32	ØS-30-21L-8Wm-450	450	2
33	ØS-30-21L-8Wm-525	525	2
34	ØS-30-21L-8Wm-600	600	2
35	ØS-30-21L-8Wm-675	675	2
36	ØS-30-21L-8Wm-790	790	2
37	ØS-30-21L-8Wm-900	900	2
38	ØS-30-21L-8Wm-1015	1015	2
39	ØS-30-21L-8Wm-1165	1165	2
40	ØS-30-21L-8Wm-1390	1390	2
41	ØS-GG-10-10Wm-130	130	3
42	ØS-GG-10-10Wm-220	220	3
43	ØS-GG-10-10Wm-300	300	3
44	ØS-GG-10-10Wm-430	430	3
45	ØS-GG-10-10Wm-520	520	3
46	ØS-GG-10-10Wm-630	630	3
47	ØS-GG-10-10Wm-700	700	3
48	ØS-GG-10-10Wm-800	800	3
49	ØS-GG-10-10Wm-910	910	3
50	ØS-GG-10-10Wm-1000	1000	3
51	ØS-GG-10-10Wm-1170	1170	3
52	ØS-GG-10-10Wm-1300	1300	3
53	ØS-GG-10-10Wm-1420	1420	3
54	ØS-GG-10-10Wm-1600	1600	3
55	ØS-GG-10-10Wm-1820	1820	3
56	ØS-Snøkabel-Lett-30-30Wm-230V-1050	1050	4
57	ØS-Snøkabel-Lett-30-30Wm-230V-1500	1500	4
58	ØS-Snøkabel-Lett-30-30Wm-230V-1800	1800	4
59	ØS-Snøkabel-Lett-30-30Wm-230V-2100	2100	4
60	ØS-Snøkabel-Lett-30-30Wm-230V-2400	2400	4
61	ØS-Snøkabel-Lett-30-30Wm-230V-2700	2700	4
62	ØS-Snøkabel-Lett-30-30Wm-230V-3000	3000	4
63	ØS-Snøkabel-Lett-30-30Wm-230V-3600	3600	4
64	ØS-Snøkabel-Lett-30-30Wm-230V-4500	4500	4
65	ØS-Snøkabel-Lett-30-30Wm-230V-5100	5100	4
66	ØS-Snøkabel-Lett-30-30Wm-230V-6000	6000	4
67	ØS-Snøkabel-Lett-30-30Wm-400V-2700	2700	5
68	ØS-Snøkabel-Lett-30-30Wm-400V-3000	3000	5
69	ØS-Snøkabel-Lett-30-30Wm-400V-3600	3600	5
70	ØS-Snøkabel-Lett-30-30Wm-400V-4500	4500	5
71	ØS-Snøkabel-Lett-30-30Wm-400V-5100	5100	5
72	ØS-Snøkabel-Lett-30-30Wm-400V-6000	6000	5
73	ØS-Snømatte-300Wkvm-400V-2700	2700	6
74	ØS-Snømatte-300Wkvm-400V-3000	3000	6
75	ØS-Snømatte-300Wkvm-400V-3600	3600	6
76	ØS-Snømatte-300Wkvm-400V-3000	3000	6
77	ØS-Snømatte-300Wkvm-400V-3600	3600	6
78	ØS-Snømatte-300Wkvm-400V-4500	4500	6
79	ØS-Snømatte-300Wkvm-400V-5100	5100	6
80	ØS-Snømatte-300Wkvm-400V-6000	6000	6
81	ØS-Snømatte-300Wkvm-1050	1050	7
82	ØS-Snømatte-300Wkvm-1500	1500	7
83	ØS-Snømatte-300Wkvm-1800	1800	7
84	ØS-Snømatte-300Wkvm-2100	2100	7
85	ØS-Snømatte-300Wkvm-2400	2400	7
86	ØS-Snømatte-300Wkvm-2700	2700	7
87	ØS-Snømatte-300Wkvm-3000	3000	7
88	ØS-Snømatte-300Wkvm-3600	3600	7
89	ØS-Snømatte-300Wkvm-3000	3000	7
90	ØS-Snømatte-300Wkvm-3600	3600	7
91	ØS-Snømatte-300Wkvm-4500	4500	7
92	ØS-Snømatte-300Wkvm-5100	5100	7
93	ØS-Snømatte-300Wkvm-6000	6000	7
94	ØS-Varmematte-120Wkvm-60	60	8
95	ØS-Varmematte-120Wkvm-120	120	8
96	ØS-Varmematte-120Wkvm-180	180	8
97	ØS-Varmematte-120Wkvm-240	240	8
98	ØS-Varmematte-120Wkvm-300	300	8
99	ØS-Varmematte-120Wkvm-360	360	8
100	ØS-Varmematte-120Wkvm-420	420	8
101	ØS-Varmematte-120Wkvm-480	480	8
102	ØS-Varmematte-120Wkvm-600	600	8
103	ØS-Varmematte-120Wkvm-720	720	8
104	ØS-Varmematte-120Wkvm-840	840	8
105	ØS-Varmematte-120Wkvm-960	960	8
106	ØS-Varmematte-120Wkvm-1080	1080	8
107	ØS-Varmematte-120Wkvm-1200	1200	8
108	ØS-Varmematte-120Wkvm-1320	1320	8
109	ØS-Varmematte-120Wkvm-1440	1440	8
110	ØS-Varmematte-80Wkvm-40	40	9
111	ØS-Varmematte-80Wkvm-80	80	9
112	ØS-Varmematte-80Wkvm-120	120	9
113	ØS-Varmematte-80Wkvm-160	160	9
114	ØS-Varmematte-80Wkvm-200	200	9
115	ØS-Varmematte-80Wkvm-240	240	9
116	ØS-Varmematte-80Wkvm-280	280	9
117	ØS-Varmematte-80Wkvm-320	320	9
118	ØS-Varmematte-80Wkvm-400	400	9
119	ØS-Varmematte-80Wkvm-480	480	9
120	ØS-Varmematte-80Wkvm-560	560	9
121	ØS-Varmematte-80Wkvm-640	640	9
122	ØS-Varmematte-80Wkvm-720	720	9
123	ØS-Varmematte-80Wkvm-800	800	9
124	ØS-Varmematte-80Wkvm-880	880	9
125	ØS-Varmematte-80Wkvm-960	960	9
126	TXLP/2R 230/10	230	10
127	TXLP/2R 380/10	380	10
128	TXLP/2R 530/10	530	10
129	TXLP/2R 650/10	650	10
130	TXLP/2R 760/10	760	10
131	TXLP/2R 940/10	940	10
132	TXLP/2R 1050/10	1050	10
133	TXLP/2R 1300/10	1300	10
134	TXLP/2R 1610/10	1610	10
135	TXLP/2R 200/17	200	11
136	TXLP/2R 300/17	300	11
137	TXLP/2R 400/17	400	11
138	TXLP/2R 500/17	500	11
139	TXLP/2R 600/17	600	11
140	TXLP/2R 700/17	700	11
141	TXLP/2R 840/17	840	11
142	TXLP/2R 1000/17	1000	11
143	TXLP/2R 1250/17	1250	11
144	TXLP/2R 1370/17	1370	11
145	TXLP/2R 1500/17	1500	11
146	TXLP/2R 1700/17	1700	11
147	TXLP/2R 2100/17	2100	11
148	TXLP/2R 2600/17	2600	11
149	TXLP/2R 3300/17	3300	11
\.


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: runarkristoffersen
--

SELECT pg_catalog.setval('products_id_seq', 149, true);


--
-- Name: manufacturors manufacturors_pkey; Type: CONSTRAINT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY manufacturors
    ADD CONSTRAINT manufacturors_pkey PRIMARY KEY (id);


--
-- Name: product_specs product_specs_pkey; Type: CONSTRAINT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY product_specs
    ADD CONSTRAINT product_specs_pkey PRIMARY KEY (id);


--
-- Name: product_types product_types_pkey; Type: CONSTRAINT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY product_types
    ADD CONSTRAINT product_types_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: product_specs product_specs_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY product_specs
    ADD CONSTRAINT product_specs_product_id_fkey FOREIGN KEY (product_id) REFERENCES products(id);


--
-- Name: product_types product_types_manufacturor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY product_types
    ADD CONSTRAINT product_types_manufacturor_id_fkey FOREIGN KEY (manufacturor_id) REFERENCES manufacturors(id);


--
-- Name: products products_product_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: runarkristoffersen
--

ALTER TABLE ONLY products
    ADD CONSTRAINT products_product_type_id_fkey FOREIGN KEY (product_type_id) REFERENCES product_types(id);


--
-- PostgreSQL database dump complete
--

