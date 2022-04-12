from typing import Optional, List
from spacy.tokens import Token
from .general import WordMatch, WordMatchingStrategy
from ..parsing import MultiwordSpan, Subword, SearchPhrase


class DerivationWordMatchingStrategy(WordMatchingStrategy):

    WORD_MATCH_TYPE_LABEL = "derivation"

    def match_multiwords(
        self,
        search_phrase: SearchPhrase,
        search_phrase_token: Token,
        document_token: Token,
        document_multiwords: List[MultiwordSpan],
    ) -> Optional[WordMatch]:

        if len(search_phrase_token._.holmes.lemma.split()) == 1:
            return None
        if search_phrase_token._.holmes.derivation_matching_reprs is None and not any(
            m for m in document_multiwords if m.derivation_matching_reprs is not None
        ):
            return None

        if search_phrase_token._.holmes.derivation_matching_reprs is not None:
            search_phrase_reprs = search_phrase_token._.holmes.derivation_matching_reprs
        else:
            search_phrase_reprs = search_phrase_token._.holmes.direct_matching_reprs

        for (
            search_phrase_representation
        ) in search_phrase_token._.holmes.direct_matching_reprs:
            for multiword in document_multiwords:
                if multiword.derivation_matching_reprs is not None:
                    document_reprs = multiword.derivation_matching_reprs
                else:
                    document_reprs = multiword.direct_matching_reprs
                for document_representation in document_reprs:
                    if search_phrase_representation == document_representation:
                        search_phrase_display_word = (
                            search_phrase_token._.holmes.lemma.upper()
                        )
                        return WordMatch(
                            search_phrase_token=search_phrase_token,
                            search_phrase_word=search_phrase_representation,
                            document_token=document_token,
                            first_document_token=document_token.doc[
                                multiword.token_indexes[0]
                            ],
                            last_document_token=document_token.doc[
                                multiword.token_indexes[-1]
                            ],
                            document_subword=None,
                            document_word=document_representation,
                            word_match_type=self.WORD_MATCH_TYPE_LABEL,
                            explanation=self._get_explanation(
                                search_phrase_display_word
                            ),
                        )
        return None

    def match_token(
        self,
        search_phrase: SearchPhrase,
        search_phrase_token: Token,
        document_token: Token,
    ) -> Optional[WordMatch]:

        if (
            search_phrase_token._.holmes.derivation_matching_reprs is None
            and document_token._.holmes.derivation_matching_reprs is None
        ):
            return None

        if search_phrase_token._.holmes.derivation_matching_reprs is not None:
            search_phrase_reprs = search_phrase_token._.holmes.derivation_matching_reprs
        else:
            search_phrase_reprs = search_phrase_token._.holmes.direct_matching_reprs

        if document_token._.holmes.derivation_matching_reprs is not None:
            document_reprs = document_token._.holmes.derivation_matching_reprs
        else:
            document_reprs = document_token._.holmes.direct_matching_reprs

        for search_phrase_representation in search_phrase_reprs:
            for document_representation in document_reprs:
                if search_phrase_representation == document_representation:
                    search_phrase_display_word = (
                        search_phrase_token._.holmes.lemma.upper()
                    )
                    return WordMatch(
                        search_phrase_token=search_phrase_token,
                        search_phrase_word=search_phrase_representation,
                        document_token=document_token,
                        first_document_token=document_token,
                        last_document_token=document_token,
                        document_subword=None,
                        document_word=document_representation,
                        word_match_type=self.WORD_MATCH_TYPE_LABEL,
                        explanation=self._get_explanation(search_phrase_display_word),
                    )
        return None

    def match_subword(
        self,
        search_phrase: SearchPhrase,
        search_phrase_token: Token,
        document_token: Token,
        document_subword: Subword,
    ) -> Optional[WordMatch]:

        if (
            search_phrase_token._.holmes.derivation_matching_reprs is None
            and document_subword.derivation_matching_reprs is None
        ):
            return None

        if search_phrase_token._.holmes.derivation_matching_reprs is not None:
            search_phrase_reprs = search_phrase_token._.holmes.derivation_matching_reprs
        else:
            search_phrase_reprs = search_phrase_token._.holmes.direct_matching_reprs

        if document_subword.derivation_matching_reprs is not None:
            document_reprs = document_subword.derivation_matching_reprs
        else:
            document_reprs = document_subword.holmes.direct_matching_reprs

        for search_phrase_representation in search_phrase_reprs:
            for document_representation in document_reprs:
                if search_phrase_representation == document_representation:
                    search_phrase_display_word = (
                        search_phrase_token._.holmes.lemma.upper()
                    )
                    return WordMatch(
                        search_phrase_token=search_phrase_token,
                        search_phrase_word=search_phrase_representation,
                        document_token=document_token,
                        first_document_token=document_token,
                        last_document_token=document_token,
                        document_subword=document_subword,
                        document_word=document_representation,
                        word_match_type=self.WORD_MATCH_TYPE_LABEL,
                        explanation=self._get_explanation(search_phrase_display_word),
                    )
        return None

    def add_words_matching_search_phrase_root_token(self, search_phrase: SearchPhrase):
        if (
            search_phrase.root_token._.holmes.derived_lemma
            != search_phrase.root_token._.holmes.lemma
        ):
            search_phrase.add_word_information(
                search_phrase.root_token._.holmes.derived_lemma,
                self.WORD_MATCH_TYPE_LABEL,
                0,
            )

    @staticmethod
    def _get_explanation(search_phrase_display_word: str) -> str:
        return "".join(("Has a common stem with ", search_phrase_display_word, "."))
