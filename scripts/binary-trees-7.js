/* The Computer Language Benchmarks Game
   https://salsa.debian.org/benchmarksgame-team/benchmarksgame/

   contributed by Léo Sarrazin
   multi thread by Andrey Filatkin
   sequential by Isaac Gouy
*/

function runBenchmark() {
    function mainThread() {
        const n = 8;
        const maxDepth = Math.max(6, n);

        const stretchDepth = maxDepth + 1;
        const check = itemCheck(bottomUpTree(stretchDepth));

        const longLivedTree = bottomUpTree(maxDepth);

        for (let depth = 4; depth <= maxDepth; depth += 2) {
            const iterations = 1 << (maxDepth - depth + 4);
            work(iterations, depth);
        }
    }

    function work(iterations, depth) {
        let check = 0;
        for (let i = 0; i < iterations; i++) {
            check += itemCheck(bottomUpTree(depth));
        }
    }

    function TreeNode(left, right) {
        return { left, right };
    }

    function itemCheck(node) {
        if (node.left === null) {
            return 1;
        }
        return 1 + itemCheck(node.left) + itemCheck(node.right);
    }

    function bottomUpTree(depth) {
        return depth > 0 ? new TreeNode(bottomUpTree(depth - 1), bottomUpTree(depth - 1)) : new TreeNode(null, null);
    }

    mainThread();
}

runBenchmark();
