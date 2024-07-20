---
layout: page
title: Search
permalink: /search/
---

<input type="text" id="search-input" onkeyup="search(event)" placeholder="Search...">
<div id="results"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/lunr.js/2.3.8/lunr.min.js"></script>
<script>
    let idx;
    let documents;

    async function fetchIndexAndDocuments() {
    if (!idx) {
        const response = await fetch('{{ "/search.json" | relative_url }}');
        documents = await response.json();

        idx = lunr(function () {
            this.ref('url');
            this.field('title');
            this.field('content');

            documents.forEach(function (doc) {
                this.add(doc);
            }, this);
        });

        window.documents = documents;
    }
    }

    async function search(event) {
    await fetchIndexAndDocuments();
    const query = event.target.value;
    if(query === '') {
        document.getElementById('results').innerHTML = '';
        return;
    }

    const results = idx.search(query).map(result => {
        return documents.find(doc => doc.url === result.ref);
    });

    console.log('Search idx:', idx);
    console.log('Search query:', query);
    console.log('Search results:', results);

    const resultsContainer = document.getElementById('results');
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No results found</p>';
    } else {
        resultsContainer.innerHTML = results.map(result => {
        return `<div><a href="${result.url}">${result.title}</a></div>`;
        }).join('');
    }
    }
</script>
