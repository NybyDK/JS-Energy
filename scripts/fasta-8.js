/* The Computer Language Benchmarks Game
   https://salsa.debian.org/benchmarksgame-team/benchmarksgame/

   Naive transliteration from Drake Diedrich's C program
   contributed by Isaac Gouy 
*/

function runBenchmark() {
    const IM = 139968;
    const IA = 3877;
    const IC = 29573;
    const SEED = 42;

    let seed = SEED;
    function fastaRand(max) {
        seed = (seed * IA + IC) % IM;
        return (max * seed) / IM;
    }

    const ALU =
        "GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGG" +
        "GAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGA" +
        "CCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAAT" +
        "ACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCA" +
        "GCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGG" +
        "AGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCC" +
        "AGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAA";

    const iub = "acgtBDHKMNRSVWY";
    const iubP = [0.27, 0.12, 0.12, 0.27, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02];

    const homosapiens = "acgt";
    const homosapiensP = [0.302954942668, 0.1979883004921, 0.1975473066391, 0.3015094502008];

    const LINELEN = 60;

    // slowest character-at-a-time output
    function repeatFasta(seq, n) {
        const len = seq.length;
        let i;
        /* explicit line buffer */
        let b = "";
        for (i = 0; i < n; i++) {
            b += seq[i % len];
            if (i % LINELEN == LINELEN - 1) {
                b += "\n";
                b = "";
            }
        }
        if (i % LINELEN != 0) {
            b += "\n";
        }
    }

    function randomFasta(seq, probability, n) {
        const len = seq.length;
        let i, j;
        /* explicit line buffer */
        let b = "";
        for (i = 0; i < n; i++) {
            let v = fastaRand(1.0);
            /* slowest idiomatic linear lookup.  Fast if len is short though. */
            for (j = 0; j < len - 1; j++) {
                v -= probability[j];
                if (v < 0) break;
            }
            b += seq[j];
            if (i % LINELEN == LINELEN - 1) {
                b += "\n";
                b = "";
            }
        }
        if (i % LINELEN != 0) {
            b += "\n";
        }
    }

    function main(n) {
        repeatFasta(ALU, n * 2);
        randomFasta(iub, iubP, n * 3);
        randomFasta(homosapiens, homosapiensP, n * 5);
    }

    main(25000);
}

runBenchmark();
